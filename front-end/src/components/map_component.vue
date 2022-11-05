<template>
    <div class="wrapper">
        <div class="left-side-wrapper">
            <div class="filter-container">
                <div class="input-container">
                    <label for="ensemble-predict">Агрегированный рейтинг привлекательности</label>
                    <input type="range" name="ensemble-predict" id="ensemble-predict">
                </div>
                <div class="input-container">
                    <label for="competitor-coverage-level">Уровень покрытия конкурентами</label>
                    <input type="range" name="competitor-coverage-level" id="competitor-coverage-level">
                </div>
                <div class="input-container">
                    <label for="objects-indication">Типы отображаемых объектов</label>
                    <select name="objects-indication" id="objects-indication">

                    </select>
                </div>
                <div class="input-container">
                    <label for="population-house-living-square">Плотность населения</label>
                    <select name="population-house-living-square" id="population-house-living-square">
                        
                    </select>
                </div>
                <div class="input-container" id="competitor-new-postmachine-usage">
                    <label for="competitor-new-postmachine-usage">Учитывать переход конкурентов на МосПостамат</label>
                    <input type="checkbox" name="competitor-new-postmachine-usage" id="competitor-new-postmachine-usage">
                </div>
                <div class="input-container">
                    <label for="postmachine-number">Кол-во устанавливаемых постаматов</label>
                    <input type="number" name="postmachine-number" id="postmachine-number">
                </div>
                <div class="submit-button-container">
                    <button id="submit-button">Получить результаты</button>
                </div>
            </div>
            <div class="download-options">
                <div class="excel-download-container">
                    <button class="excel-download-button">
                        excel
                    </button>
                </div>
                <div class="pdf-download-container">
                    <button class="pdf-print-button">
                        pdf
                    </button>
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

    import axios from 'axios';

    export default {
        name: "Map",
        
        mounted() {
            
            // Initializing map
            const map = L.map('map', {
                renderer: L.canvas(),
                drawControl: false,
            });
            
            const center_lat = 55.7558;
            const center_lon = 37.6173;
            const start_zoom = 10;
            const max_zoom = 17;
            map.setView([center_lat, center_lon], start_zoom);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: max_zoom,
            }).addTo(map);

            var regions_layer;
            var hexagons_layer = {};
            var predictions_layer = {};
            const baseLayers = {};

            layerControl = L.control.layers(baseLayers).addTo(map);

            $('.pdf-print-button').click(() => {
                window.print();
            });

            $('.submit-button').click(() => {
                const ensemble_predict = $('input[name=""]');
                const competitor_coverage_level = '';
                const objects_indication = '';
                const population_house_living_square = '';
                const competitor_new_postmachine_usage = '';
                const postmachine_number = '';

                let data = {
                    'ensemble_predict': '',
                    'competitor_coverage_level': '',
                    'objects_indication': '',
                    'population_house_living_square': '',
                    'competitor_new_postmachine_usage': '',
                    'postmachine_number': '',
                };
            })

            // ensemble-predict
            // competitor-coverage-level
            // objects-indication
            // population-house-living-square
            // competitor-new-postmachine-usage
            // postmachine-number

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
                            generateTable(e, 'region', 'object');
                        });
                    }
                });
                regions_layer.addTo(map);
                layerControl.addBaseLayer(regions_layer, 'Регионы').addTo(map);
            });

            var layerControl;
            
            axios.get(import.meta.env.VITE_api_get_objects)
            .then((response) => {
                let marker_types = [];
                for (let x in response.data) {
                    marker_types.push(response.data[x].features[0].properties.type)
                }
                let markers = {};
                for (let x in marker_types) {
                    markers[marker_types[x]] = L.markerClusterGroup();
                }
                for (let y in response.data) {
                    for (let z in response.data[y].features) {
                        var a = response.data[y].features[z].geometry.coordinates;
                        var marker = L.marker(new L.LatLng(a[1], a[0]), {properties: response.data[y].features[z].properties, geometry: response.data[y].features[z].geometry, title: `${response.data[y].features[z].properties.type}\n${response.data[y].features[z].properties.name}\n${response.data[y].features[z].properties.geometry_name}`});
                        marker.on('click', (e) => {
                            generateTable(e, 'marker', 'object');
                        });                 
                        markers[marker_types[y]].addLayer(marker);
                    }
                    layerControl.addOverlay(markers[marker_types[y]], marker_types[y]);
                }
            })
            .catch((err) => {
                console.log(err);
            });

            //create color ramp
            const getColor = (predict_value) => {
                return predict_value == 
                    undefined ?         '#000' :
                    predict_value < 10   ? '#616161' :
                    predict_value < 20   ? '#818181' :
                    predict_value < 30   ? '#a1a1a1' :
                    predict_value < 40   ? '#c7e9b4' :
                    predict_value < 50  ? '#7fcdbb' :
                    predict_value < 60  ? '#41b6c4' :
                    predict_value < 70  ? '#1d91c0' :
                    predict_value < 80 ? '#225ea8' :
                                        '#0c2c84' ;
            }

            const prediction_coords = [];

            axios.get(import.meta.env.VITE_api_get_predictions)
            .then((response) => {
                for (let x in response.data) {
                    hexagons_layer[x] = L.geoJSON(response.data[x].features, {
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
                                zoomToFeature(e, 'default');
                                generateTable(e, 'region', 'hexagon');
                            });
                        }
                    });
                }
                for (let x in response.data[2].features) {
                    prediction_coords.push([ 
                        turf.center(response.data[2].features[x]).geometry.coordinates[1],
                        turf.center(response.data[2].features[x]).geometry.coordinates[0], 
                        response.data[2].features[x].properties.ensemble_predict * 2]);
                }
                layerControl.addBaseLayer(hexagons_layer[0], `Соты [h7]`).addTo(map);
                layerControl.addBaseLayer(hexagons_layer[1], `Соты [h8]`).addTo(map);
                layerControl.addBaseLayer(hexagons_layer[2], `Соты [h9]`).addTo(map);
            });

            setTimeout(() => {
                var heat = L.heatLayer(prediction_coords,{
                    radius: 30,
                    blur: 15, 
                    maxZoom: max_zoom,
                });
                layerControl.addBaseLayer(heat, `Тепловая карта`).addTo(map);
            }, 500);

            // map.on('zoomend', (e) => {
            //     var currentZoom = map.getZoom();
            //     hexagon_layer_control(currentZoom);
            // });

            map.on('mousemove', (e) => {
                if (
                    map.hasLayer(hexagons_layer[0]) || 
                    map.hasLayer(hexagons_layer[1]) || 
                    map.hasLayer(hexagons_layer[2]) ||
                    map.hasLayer(predictions_layer)
                ) {
                    if (map.hasLayer(hexagons_layer[2])
                    ) {
                        map.setZoom(11);
                    }
                    hexlegend.addTo(map);
                } else {
                    hexlegend.remove();
                }
            });

            //legend//

            //create legend
            var hexlegend = L.control({
                position: 'bottomright'
            });

            //generate legend contents
            hexlegend.onAdd = function (map) {
                //set up legend grades and labels
                var div = L.DomUtil.create('div', 'info legend'),
                    grades = [20, 30, 40, 50, 60, 70, 80],
                    labels = ['<strong>Point Count</strong>'],
                    from, to;
                
                //iterate through grades and create a color field and label for each
                for (var i = 0; i < grades.length; i++) {
                    from = grades[i];
                    to = grades[i + 1];
                    labels.push(
                        '<i style="background:' + getColor(from + 0.5) + '"></i> ' + from + (to ? '&ndash;' + to : '+'));
                }
                div.innerHTML = labels.join('<br>');
                return div;
            };

            //attach styles and popups to the hex layer
            function highlightHex(e) {
                var layer = e.target;
                resetLayerStyles(e);
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

            const hexagon_layer_control = (currentZoom) => {
                if (
                    map.hasLayer(hexagons_layer[0]) || 
                    map.hasLayer(hexagons_layer[1]) ||
                    map.hasLayer(hexagons_layer[2])
                ) {
                    switch (currentZoom) {
                        case 13:
                        case 14:
                        case 15:
                            if (map.hasLayer(hexagons_layer[0])) {
                                hexagons_layer[0].remove();
                                hexagons_layer[1].addTo(map);
                                layerControl.removeLayer(hexagons_layer[0], `Соты`);
                                layerControl.addBaseLayer(hexagons_layer[1], `Соты`).addTo(map);
                            } 
                            else if (map.hasLayer(hexagons_layer[2])) {
                                hexagons_layer[2].remove();
                                hexagons_layer[1].addTo(map);
                                layerControl.removeLayer(hexagons_layer[2], `Hexagons`);
                                layerControl.addBaseLayer(hexagons_layer[1], `Hexagons`).addTo(map);
                            }
                            break;
                        case 16:
                        case 17:
                            if (map.hasLayer(hexagons_layer[1])) {
                                hexagons_layer[1].remove();
                                hexagons_layer[2].addTo(map);
                                layerControl.removeLayer(hexagons_layer[1], `Hexagons`);
                                layerControl.addBaseLayer(hexagons_layer[2], `Hexagons`).addTo(map);
                            } else if (map.hasLayer(hexagons_layer[0])) {
                                hexagons_layer[0].remove();
                                hexagons_layer[2].addTo(map);
                                layerControl.removeLayer(hexagons_layer[0], `Hexagons`);
                                layerControl.addBaseLayer(hexagons_layer[2], `Hexagons`).addTo(map);
                            }
                            break;
                        default:
                            if (map.hasLayer(hexagons_layer[1])) {
                                hexagons_layer[1].remove();
                                hexagons_layer[0].addTo(map);
                                layerControl.removeLayer(hexagons_layer[1], `Соты`);
                                layerControl.addBaseLayer(hexagons_layer[0], `Соты`).addTo(map);
                            } else if (map.hasLayer(hexagons_layer[2])) {
                                hexagons_layer[2].remove();
                                hexagons_layer[0].addTo(map);
                                layerControl.removeLayer(hexagons_layer[2], `Hexagons`);
                                layerControl.addBaseLayer(hexagons_layer[0], `Hexagons`).addTo(map);
                            }
                    }
                }
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
                } else if (parent_layer === 'prediction_point') {
                    let layer = e.target;
                    reset_predictions_layer();
                    layer.setStyle({
                        fillColor: 'white', 
                        color: 'black', 
                        weight: 5, 
                        opacity: 1, 
                        fillOpacity: 0.25
                    });
                } 
            };

            const reset_predictions_layer = () => {
                for (let x in predictions_layer._layers) {
                    let predict_value = predictions_layer._layers[x].feature.properties.ensemble_predict * 100;
                    predictions_layer._layers[x].setStyle({
                        radius: 10,
                        color: 'darkgrey',
                        weight: 3,
                        opacity: 0,
                        fillColor: getColor(predict_value),
                        fillOpacity: 0.5
                    });
                }
            }

            const resetLayerStyles = (e) => {
                for (let x in e.target._eventParents) {
                    e.target._eventParents[x].resetStyle();
                }
            }

            const generateTable = (e, layer_type, obj_hex) => {
                let control_number;

                if (obj_hex === 'object') {
                    control_number = 0;
                } else {
                    control_number = 1;
                }

                if (layer_type === 'region') {
                    var properties = e.target.feature.properties;
                } else if (layer_type === 'marker') {
                    var properties = e.target.options.properties;
                } else if (layer_type === 'prediction_point') {
                    var properties = e.target.properties;
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
                    // hexagons_layer[2].resetStyle();
                    reset_predictions_layer();
                });
            }

            $(document).ready(() => {
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
            });
            map.spin = false;
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
        padding: 2%;
        width: 300px;
        display: grid;
    }

    .input-container {
        margin-top: 5%;
        display: grid;
        font-size: 14px;
        user-select: none;
    }

    .input-container input,
    .input-container select {
        margin-top: 3%;
    }

    .submit-button-container {
        width: 100%;
        display: inline-flex;
        justify-content: center;
        margin-top: 15%;
    }

    #competitor-new-postmachine-usage {
        display: inline-flex;
    }

    .download-options {
        width: 100%;
        display: inline-flex;
        justify-content: space-evenly;
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

    .noramlize_name {
        max-width: 100px;
        padding-left: 15px;
        word-wrap: break-word;
    }

</style>
