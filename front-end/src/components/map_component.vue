<template>
    <div class="wrapper">
        <div class="left-side-wrapper">
            <div class="download-options">
                <div class="excel-download-container">
                    <button class="excel-download-button">
                        Выгрузка в excel
                    </button>
                </div>
                <div class="pdf-download-container">
                    <button class="pdf-print-button">
                        Выгрузка в pdf
                    </button>
                </div>
            </div>
            <div class="object-filter-container">
                <p id="object-filter-title">Отображение объектов на карте:</p>
                <div class="input-checkbox-container-container">
                </div>
                <div class="input-container model-filter-container">
                    <label for="model-filter" id="model-filter-title">Модель для расчёта</label>
                    <select name="model-filter" id="model-filter">
                        <option value="ensemble_predict" default>Основная модель (Ансамбль + Бустинг + С.Лес)</option>
                        <option value="ensemble_predict_void_postamats">Основная модель + Отсутсвие постаматов</option>
                        <option value="ensemble_predict_cannibalism_postamats">Основная модель + Перевод конкурентов</option>
                        <option value="ensemble_logreg">Ансамбль + ЛогРег</option>
                        <option value="stacking">Стекинг</option>
                        <option value="tensorflow">Нейронная сеть (0/1)</option>
                    </select>
                </div>
            </div>
            <div class="postmachine-number">
                <div class="input-container">
                    <label for="postmachine-number">Кол-во устанавливаемых постаматов</label>
                    <input type="number" name="postmachine-number" id="postmachine-number" value="100">
                </div>
            </div>
        </div>
        <div id="map">
        </div>
        <div class="datatable-container">
            <table class="datatable" id="datatable">
                <thead>

                </thead>
                <tbody>

                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

    // "ensemble_predict" - "Основная модель (Ансамбль + Бустинг + С.Лес)"
    // "ensemble_predict_void_postamats" - "Основная модель + Отсутсвие постаматов"
    // "ensemble_predict_cannibalism_postamats" - "Основная модель + Перевод конкурентов"
    // "ensemble_logreg" - "Ансамбль + ЛогРег"
    // "stacking" - "Стекинг"
    // "tensorflow" - "Нейронная сеть (0/1)"

    import axios from 'axios';
    
    export default {
        name: "Map",
        
        mounted() {

            const jsonToCsv = (items) => {
                const header = Object.keys(items[0]);

                const headerString = header.join(',');

                // handle null or undefined values here
                const replacer = (key, value) => value ?? '';

                const rowItems = items.map((row) =>
                    header
                    .map((fieldName) => JSON.stringify(row[fieldName], replacer))
                    .join(',')
                );

                // join header and body, and break into separate lines
                const csv = [headerString, ...rowItems].join('\r\n');

                return csv;
            }

            const obj = [
                { color: 'red', maxSpeed: 120, age: 2 },
                { color: 'blue', maxSpeed: 100, age: 3 },
                { color: 'green', maxSpeed: 130, age: 2 },
            ];

            const csv = jsonToCsv(obj);

            const map = L.map('map', {
                renderer: L.canvas(),
                drawControl: false,
            });
            
            const center_lat = 55.7558;
            const center_lon = 37.6173;
            const start_zoom = 11;
            const max_zoom = 17;
            map.setView([center_lat, center_lon], start_zoom);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: max_zoom,
            }).addTo(map);

            var regions_layer;
            var hexagons_layer = {};
            const baseLayers = {};

            const download = (filename, text) => {
                var element = document.createElement('a');
                element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
                element.setAttribute('download', filename);

                element.style.display = 'none';
                document.body.appendChild(element);

                element.click();

                document.body.removeChild(element);
            }

            // Start file download.
            // document.querySelector(".excel-download-button").addEventListener("click", function(){
            //     // Generate download of csv file with the content
            //     var filename = "africanfox.csv";
                
            //     download(filename, csv);
            // }, false);

            layerControl = L.control.layers(baseLayers).addTo(map);

            $('.pdf-print-button').click(() => {
                window.print();
            });

            axios.get(import.meta.env.VITE_api_get_regions)
            .then((response) => {
                regions_layer = L.geoJSON(response.data, {
                    style: (feature) => {
                        return {
                            color: '#707070', 
                            fillColor: 'lightskyblue', 
                            weight: 2, 
                            opacity: 0.7, 
                            fillOpacity: 0.25
                        };
                    },
                    onEachFeature: (feature, layer) => {
                        layer.on("click", (e) => {
                            zoomToFeature(e, 'default');
                            generateTable(e, 'region');
                        });
                    }
                });
                layerControl.addBaseLayer(regions_layer, 'Регионы').addTo(map);
            });

            var layerControl;

            $('.input-checkbox-container-container').append('<p style="margin: 100px 20px">Data is being loaded</p>');
            
            const objects_checked = {};
            let save_response;
            let marker_types = [];

            axios.get(import.meta.env.VITE_api_get_objects)
            .then((response) => {
                save_response = response.data;
                for (let x in response.data) {
                    marker_types.push(response.data[x].features[0].properties.type);
                }
                let markers = {};
                for (let x in marker_types) {
                    markers[marker_types[x]] = L.markerClusterGroup();
                }
                let objects_input_content = {};
                for (let y in response.data) {
                    for (let z in response.data[y].features) {
                        var a = response.data[y].features[z].geometry.coordinates;
                        var marker = L.marker(new L.LatLng(a[1], a[0]), {
                            properties: response.data[y].features[z].properties, 
                            geometry: response.data[y].features[z].geometry, 
                            title: `${response.data[y].features[z].properties.type}\n${response.data[y].features[z].properties.name}\n${response.data[y].features[z].properties.geometry_name}`
                        });
                        marker.on('click', (e) => {
                            generateTable(e, 'marker');
                        });                 
                        markers[marker_types[y]].addLayer(marker);
                    }
                    objects_input_content[y] = 
                    `<div class="input-container markers-checkbox-container" id="objects-indication-input-container">
                        <label for="markers-${y}">${marker_types[y]}</label>
                        <input class="markers-checkbox" type="checkbox" name="markers" id="markers-${y}" value="${y}">
                    </div>`
                }

                let objects_input_content_final =  objects_input_content[2] + objects_input_content[1] + objects_input_content[0] + objects_input_content[3];

                $('.input-checkbox-container-container').empty();
                $('.input-checkbox-container-container').append(objects_input_content_final);

                document.querySelector('label[for="markers-3"]').innerText = "Жилые дома";

                $(document).on('click','input[name="markers"]', function(e){
                    if (this.checked === true) {
                        markers[marker_types[this.value]].addTo(map);
                        objects_checked[this.value] = this.value;
                    } else {
                        markers[marker_types[this.value]].remove();
                        delete objects_checked[this.value];
                    }
                });
            })
            .catch((err) => {
                console.log(err);
            });

            //create color ramp
            const getColor = (predict_value) => {
                return predict_value == 
                    undefined           ? '#aaa' :
                    predict_value < 0.5 ? '#aaa' :
                    predict_value < 20  ? '#a0a200' :
                    predict_value < 30  ? '#b1b301' :
                    predict_value < 40  ? '#c2c402' :
                    predict_value < 50  ? '#d3d403' :
                    predict_value < 60  ? '#e4e514' :
                    predict_value < 80  ? '#f5f625' :
                    predict_value < 80  ? '#f7a416' :
                    predict_value < 95  ? '#fe8516' :
                                        '#fe3b09' ;
            }

            let prediction_coords = [];

            const hexagon_types = {
                0: 'Hexagon_7',
                1: 'Hexagon_8',
                2: 'Hexagon_9'
            }

            for (let x = 0; x < 3; x++) {
                axios.get(import.meta.env.VITE_api_get_hexagons + hexagon_types[x])
                .then((response) => {
                    hexagons_layer[x] = L.geoJSON(response.data, {
                        style: (feature) => {
                            return {
                                color: 'darkgrey',
                                weight: 1,
                                opacity: 0,
                                fillColor: getColor(feature.properties.ensemble_predict * 100),
                                fillOpacity: 0.75
                            };
                        },
                        onEachFeature: (feature, layer) => {
                            onEachHex(feature, layer);
                            layer.on("click", (e) => {
                                generateTable(e, 'region');
                            });
                        }
                    });
                    switch (x) {
                        case 0:
                            layerControl.addBaseLayer(hexagons_layer[x], `Соты [h7]`).addTo(map);
                            hexagons_layer[x].addTo(map);
                            break;
                        case 1:
                            layerControl.addBaseLayer(hexagons_layer[x], `Соты [h8]`).addTo(map);
                            break;
                        case 2:
                            layerControl.addBaseLayer(hexagons_layer[x], `Соты [h9]`).addTo(map);
                            break;
                        default:
                    }
                    if (x === 2) {
                        for (let y in response.data.features) {
                            prediction_coords.push([ 
                                turf.center(response.data.features[y]).geometry.coordinates[1],
                                turf.center(response.data.features[y]).geometry.coordinates[0], 
                                response.data.features[y].properties.ensemble_predict * 2
                            ]);
                        }
                    }
                });
            }

            var heat;

            setTimeout(() => {
                heat = L.heatLayer(prediction_coords,{
                    radius: 30,
                    blur: 15, 
                    maxZoom: max_zoom,
                });
                layerControl.addBaseLayer(heat, `Тепловая карта`).addTo(map);
            }, 15000);

            map.on('mousemove', (e) => {
                if (
                    map.hasLayer(hexagons_layer[0]) || 
                    map.hasLayer(hexagons_layer[1]) || 
                    map.hasLayer(hexagons_layer[2])
                ) {
                    hexlegend.addTo(map);
                } else {
                    hexlegend.remove();
                }
            });

            $('select[name="model-filter"]').change(() => {
                const val = $('select[name="model-filter"]').val();
                styleChange(val);
            });

            const styleChange = (val) => {
                for (let x in hexagons_layer[0]._layers) {
                    hexagons_layer[0]._layers[x].setStyle({
                        color: 'darkgrey',
                        weight: 1,
                        opacity: 0,
                        fillColor: getColor(hexagons_layer[0]._layers[x].feature.properties[val] * 100),
                        fillOpacity: 0.75
                    });
                }
                for (let x in hexagons_layer[1]._layers) {
                    hexagons_layer[1]._layers[x].setStyle({
                        color: 'darkgrey',
                        weight: 1,
                        opacity: 0,
                        fillColor: getColor(hexagons_layer[1]._layers[x].feature.properties[val] * 100),
                        fillOpacity: 0.75
                    });
                }
                prediction_coords = [];
                for (let x in hexagons_layer[2]._layers) {
                    hexagons_layer[2]._layers[x].setStyle({
                        color: 'darkgrey',
                        weight: 1,
                        opacity: 0,
                        fillColor: getColor(hexagons_layer[2]._layers[x].feature.properties[val] * 100),
                        fillOpacity: 0.75
                    });
                    prediction_coords.push([ 
                        turf.center(hexagons_layer[2]._layers[x].feature).geometry.coordinates[1],
                        turf.center(hexagons_layer[2]._layers[x].feature).geometry.coordinates[0], 
                        hexagons_layer[2]._layers[x].feature.properties[val] * 2
                    ]);
                }
                
                var heat_added = map.hasLayer(heat);
                heat.remove();
                layerControl.removeLayer(heat);          
                heat = L.heatLayer(prediction_coords,{
                    radius: 30,
                    blur: 15, 
                    maxZoom: max_zoom,
                })
                layerControl.addBaseLayer(heat, `Тепловая карта`).addTo(map);
                if (heat_added) {
                    heat.addTo(map);
                }
            };

            //legend//

            //create legend
            var hexlegend = L.control({
                position: 'bottomright'
            });

            //generate legend contents
            hexlegend.onAdd = function (map) {
                //set up legend grades and labels
                var div = L.DomUtil.create('div', 'info legend'),
                    grades = [0, 0.5, 20, 30, 40, 50, 60, 80, 80, 95],
                    labels = ['<strong>Показатель оптимальности размещения</strong><br>'],
                    from, to;
                
                //iterate through grades and create a color field and label for each
                for (var i = 0; i < grades.length; i++) {
                    from = grades[i];
                    to = grades[i + 1];
                    if (from == 0) {
                        labels.push(
                        '<i style="background:' + getColor(from) + '"></i> ' + from + ('&ndash;' + to + '%'));
                    } else {
                        labels.push(
                        '<i style="background:' + getColor(from + 0.5) + '"></i> ' + from + (to ? ('&ndash;' + to) + '%' : '%+'));
                    }
                    
                }
                div.innerHTML = labels.join('<br>');
                return div;
            };

            //attach styles and popups to the hex layer
            function highlightHex(e) {
                var layer = e.target;
                const val = $('select[name="model-filter"]').val();
                styleChange(val);
                layer.setStyle({
                    fillColor: 'white', 
                    color: 'black', 
                    weight: 5, 
                    opacity: 1, 
                    fillOpacity: 0.25
                });
            }

            function onEachHex(feature, layer) {
                layer.on({
                    click: highlightHex,
                });
            }

            const zoomToFeature = (e, parent_layer) => {
                if (parent_layer === 'default') {
                    var layer = e.target;
                    resetLayerStyles(e);
                    layer.setStyle({
                        fillColor: 'white', 
                        color: 'black', 
                        weight: 5, 
                        opacity: 1, 
                        fillOpacity: 0.25
                    });
                    map.fitBounds(e.target.getBounds());
                }
            };

            const resetLayerStyles = (e) => {
                for (let x in e.target._eventParents) {
                    e.target._eventParents[x].resetStyle();
                }
            }

            const indexOfMax = (arr) => {
                if (arr.length === 0) {
                    return -1;
                }

                var max = arr[0];
                var maxIndex = 0;

                for (var i = 1; i < arr.length; i++) {
                    if (arr[i] > max) {
                        maxIndex = i;
                        max = arr[i];
                    }
                }

                return maxIndex;
            }

            const filter_objects = () => {
                const locations_amount = $('input[name="postmachine-number"]').val();
                const check_model = $('select[name="model-filter"]').val();
                // console.log(objects_checked);
                // console.log(save_response);
                // console.log(check_model);
                const newObj = {};

                for (let x in marker_types) {
                    newObj[x] = {};
                    newObj['result_' + x] = [];
                }

                // console.log(save_response);

                for (let x in objects_checked) {
                    for (let y in save_response[x].features) {
                        newObj[x][y] = save_response[x].features[y].properties[check_model];
                    }
                }
                
                for (let x in objects_checked) {
                    for (let y = 0; y < locations_amount; y++) {
                        let arr_1 = Object.values(newObj[x]);
                        for (let z in newObj[x]) {
                            if (newObj[x][z] === Math.max(...arr_1)) {
                                newObj['result_' + x].push(newObj[x][z]);
                                delete newObj[x][z];
                            }
                        }
                    }
                    console.log(newObj['result_' + x]);
                }
            }

            $('.excel-download-button').click(filter_objects);

            const generateTable = (e, layer_type, obj_hex) => {

                if (layer_type === 'region') {
                    var properties = e.target.feature.properties;
                } else if (layer_type === 'marker') {
                    var properties = e.target.options.properties;
                } 

                $('#datatable thead').empty();
                $('#datatable tbody').empty();
                let table_head = `
                    <tr class="close-button">
                        <th>&times;</th>
                    </tr>
                `;
                $('#datatable thead').append(table_head);
                let table_body = '';
                for (let x in properties) {
                    table_body += `<tr>`;
                        table_body += `
                        <td class="${x}-header">${x}</td>
                        <td class="${x}-content">${properties[x]}</td>
                    `
                    table_body += `</tr>`
                }
                $('#datatable tbody').append(table_body);

                $('.close-button th').click((e) => {
                    $('#datatable thead').empty();
                    $('#datatable tbody').empty();

                    regions_layer.resetStyle();
                    hexagons_layer[0].resetStyle();
                    hexagons_layer[1].resetStyle();
                    hexagons_layer[2].resetStyle();
                });
            }

            $('#datatable').dataTable({
                'bSort': false,
                'aoColumns': [ 
                    { sWidth: "45%", bSearchable: false, bSortable: false }, 
                    { sWidth: "45%", bSearchable: false, bSortable: false }, 
                    { sWidth: "10%", bSearchable: false, bSortable: false } 
                ],
                "scrollY": screen.height * 0.85,
                "scrollCollapse": true,
                "info": false,
                "paging": false,
                "responsive": true,
                "lengthChange": true,
                "autoWidth": true,
                "pageLength": false,
                "searching": false,
            });
        }
    }

</script>

<style>

    .wrapper {
        display: inline-flex;
        max-height: 100vh;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .left-side-wrapper {
        padding: 1% 1.5% 3% 1.5%;
        width: 300px;
        height: 100%;
        display: grid;
    }

    .input-container {
        margin-top: 3%;
        display: grid;
        font-size: 14px;
        user-select: none;
    }

    .input-container input,
    .input-container select {
        margin-top: 3%;
    }

    #competitor-new-postmachine-usage {
        display: inline-flex;
    }

    .markers-checkbox-container {
        display: inline-flex;
        width: 100%;
        justify-content: space-between;
    }

    #model-filter,
    #model-filter option {
        height: 50px;
        max-width: 200px;
        word-wrap: break-word;
        user-select: none;
    }

    .object-filter-container {
        margin-top: 30%;
    }

    #object-filter-title {
        padding-bottom: 10%;
    }

    .model-filter-container {
        margin-top: 50%;
    }

    /* .model-filter-container::before {
        content: '';
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        border-top: thin solid black;
    } */

    /* .model-filter-container::after {
        content: '';
        margin-top: 2%;
        left: 0;
        height: 100%;
        width: 100%;
        border-bottom: thin solid black;
    } */

    .filter-container {
        margin-top: 3%;
    }

    .submit-button-container {
        width: 100%;
        display: inline-flex;
        justify-content: center;
        margin-top: 5%;
    }

    .download-options {
        margin-top: 10%;
        width: 100%;
        display: inline-flex;
        justify-content: space-evenly;
    }

    .download-options div button {
        margin: 3%;
        padding: 3% 1%;
    }

    #map {
        height: 100vh;
        width: 75%;
    }

    .info {
        padding: 6px 8px;
        font: 14px/16px Arial, Helvetica, sans-serif;
        background: white;
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
        border-radius: 5px;
    }

    .legend {
        text-align: left;
        line-height: 18px;
        color: #555;
    }

    .legend i {
        width: 18px;
        height: 18px;
        float: left;
        margin-right: 8px;
        opacity: 0.7;
    }

    .legend .colorcircle {
        border-radius: 50%;
        width: 15px;
        height: 15px;
        margin-top: 0px;
    }

    .info.legend.leaflet-control {
        width: 135px;
    }

    .info.legend.leaflet-control strong {
        margin-top: 5%;
    }

    .datatable-container {
        position: relative;
        margin-top: 1%;
        right: 0;
        height: 100%;
        width: 25%;
        overflow: hidden;
    }

    .datatable {
        padding: 0% 5% 0% 5%;
        position: relative;
        width: 100%;
        height: 100%;
    }

    .datatable tr td:first-of-type {
        border-right: thin solid black;
    }

    .datatable tr td {
        max-width: 100px;
        word-wrap: break-word;
        user-select: none;
    }

    .datatable td {
        border-bottom: thin solid black;
    }

    .datatable tr:last-of-type td {
        border-bottom: none;
    }    

    .datatable td {
        padding: 10px;
    }

    .close-button {
        position: relative;
        width: 100% !important;
        justify-content: left;
        display: flex;
    }

    .close-button th {
        font-size: 32px;
        font-weight: normal;
        cursor: pointer;
        transition: transform 0.2s ease;
    }

    .close-button th:hover {
        transform: translateY(-5%);
        transition: transform 0.2s ease;
    }

    .dataTables_empty,
    .dataTables_scrollHead {
        display: none;
    }

    .count_nearest_postamats, 
    .count_nearest_pvz, 
    .food_delivery, 
    .digitalization, 
    .covering_postamats, 
    .region_avarage_age, 
    .region_population, 
    .average_salary, 
    .average_employees, 
    .prc_employees_small_businesses, 
    .count_small_enterprises, 
    .population_density_region, .investments, 
    .price_metr_housing, 
    .cost_apartment, 
    .rating_ecology, 
    .entertainment_infrastructure, 
    .house_infrastructure_rating, 
    .prc_xenophobic, .area_per_human_region, 
    .population_region, 
    .prc_of_russians, 
    .prc_people_higher_education, 
    .death_rate, 
    .total_fertility_rate, 
    .prc_children, 
    .budget_expenditures, 
    .budget_revenues, 
    .count_nearest_metro, 
    .level_working_region, 
    .level_sleeping_region, 
    .population_house_flat, 
    .population_house_square, 
    .population_house_living_square {
        max-width: 50px;
        padding-left: 15px;
        word-wrap: break-word;
    }

    .normalize_name {
        max-width: 100px;
        padding-left: 15px;
        word-wrap: break-word;
    }

</style>
