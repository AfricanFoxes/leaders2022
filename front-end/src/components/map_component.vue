<template>
    <div class="wrapper">
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

    import * as fs from 'fs';

    export default {
        name: "Map",
        
        mounted() {

            // // Function for dynamically changing the label of the current page
            // for (var x = 0; x < document.querySelector('.active.exact-active').attributes.length; x++) {
            //     if (document.querySelector('.active.exact-active').attributes[x].name == 'modelvalue') {
            //         document.querySelector('#page-title').innerHTML = '';
            //         document.querySelector('#page-title').append(document.querySelector('.active.exact-active').attributes[x].nodeValue);
            //     }
            // }
            
            // Initializing map
            const map = L.map('map', {
                drawControl: false,
            }).setView([55.7558, 37.6173], 10);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
            }).addTo(map);

            map.spin = true;

            // Function for firing alerts
            const fireAlert = (message, icon) => {
                Swal.fire({
                    icon: icon,
                    title: message,
                    showConfirmButton: false,
                    timer: 1500
                });
            }

            var regions;

            const baseLayers = {};

            let markers_0 = L.markerClusterGroup();
            let markers_1 = L.markerClusterGroup();
            let markers_2 = L.markerClusterGroup();
            let markers_3 = L.markerClusterGroup();
            let markers_4 = L.markerClusterGroup();

            var overlays = {
                'Постамат': markers_0,
                'ПВЗ': markers_1,
                'Киоск': markers_2,
                'Дом культуры': markers_3,
                'МФЦ': markers_4,
            };

            layerControl = L.control.layers(baseLayers, overlays).addTo(map);

            axios.get(import.meta.env.VITE_api_get_regions)
            .then((response) => {

                regions = L.geoJSON(response.data, {
                    style: function (feature) {
                        return {
                            fillColor: 'lightskyblue', 
                            color: 'lightskyblue', 
                            weight: '3', 
                            opacity: 0.7, 
                            fillOpacity: 0.3
                        };
                    },
                    onEachFeature: (feature, layer) => {
                        layer.on("click", (e) => {
                            console.log(e);
                            zoomToFeature(e);
                        });
                    }
                });
                regions.addTo(map);

                layerControl.addBaseLayer(regions, 'Regions').addTo(map);
            });

            function zoomToFeature(e) {
                var layer = e.target;
                regions.resetStyle();
                layer.setStyle({
                    fillColor: 'black', 
                    color: 'black', 
                    weight: '3', 
                    opacity: 1, 
                    fillOpacity: 0.5
                });
                map.fitBounds(e.target.getBounds());
            };

            let capture_data;
            var layerControl;
            
            axios.get(import.meta.env.VITE_api_get_objects)
            .then((response) => {
                let table_content = `<tr>`;
                for (let x in response.data.features[0].properties) {
                    table_content += `
                        <th class="${x}">${x}</th>
                    `
                }
                table_content += `</tr>`
                $('#datatable thead').append(table_content);
                const data = response.data.features;
                capture_data = data;

                for (let y = 0; y < (Object.keys(data).length).toFixed(0); y++) {

                    var a = data[y].geometry.coordinates;
                    var marker = L.marker(new L.LatLng(a[1], a[0]));

                    if (data[y].properties.type === 'Постамат') {
                        markers_0.addLayer(marker);
                    } else if (data[y].properties.type === 'ПВЗ') {
                        markers_1.addLayer(marker);
                    } else if (data[y].properties.type === 'Киоск') {
                        markers_2.addLayer(marker);
                    } else if (data[y].properties.type === 'Дом культуры') {
                        markers_3.addLayer(marker);
                    } else if (data[y].properties.type === 'МФЦ') {
                        markers_4.addLayer(marker);
                    }

                    // let markers_layer_group = {
                    //     'Постамат': markers_0,
                    //     'ПВЗ': markers_1,
                    //     'Киоск': markers_2,
                    //     'Дом культуры': markers_3,
                    //     'МФЦ': markers_4,
                    // };

                    // layerControl.addOverlay(markers_0, 'Постамат');
                    // layerControl.addOverlay(markers_1, 'ПВЗ');
                    // layerControl.addOverlay(markers_2, 'Киоск');
                    // layerControl.addOverlay(markers_3, 'Дом культуры');
                    // layerControl.addOverlay(markers_4, 'МФЦ');

                    // table_content = `
                    //     <tr>
                    // `
                    // const properties = data[y].properties;

                    // for (let x in properties) {
                    //     if (x === 'digitalization') {
                    //         table_content += `
                    //             <td class="${x}">${properties[x].toFixed(2)}</td>
                    //         `
                    //     } else {
                    //         table_content += `
                    //             <td class="${x}">${properties[x]}</td>
                    //         `
                    //     }
                    // }
                    // table_content += `
                    //     </tr>
                    // `
                    // let popup_content = ``;
                    // $('#datatable tbody').append(table_content);
                }
            })
            .catch((err) => {
                console.log(err);
            });

            $(document).ready(function() {
                $('#datatable').dataTable( {
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
                } );
            } );
            
            // var canvasLayer = new L.CustomLayer({
            //     container: document.createElement("canvas"),
            //     padding: 0.1
            // });

            // canvasLayer.on("layer-render", function() {
            
            // });

            // canvasLayer.addTo(map);

                // var canvasLayer = new L.CustomLayer({
                //     container: document.createElement("canvas"),
                //     padding: 0.1
                // });

                // canvasLayer.on("layer-render", function() {
                //     var { ctx } = this.setFullLayerBounds();

                //     var canvas = this.getContainer();
                //     var dpr = L.Browser.retina ? 2 : 1;
                //     var size = this._bounds.getSize();
                //     var padding = this._padding;

                //     // set Size
                //     canvas.width = dpr * size.x;
                //     canvas.height = dpr * size.y;
                //     canvas.style.width = size.x + "px";
                //     canvas.style.height = size.y + "px";
                        
                //     var ctx = canvas.getContext("2d");

                //     // HD adaptation
                //     if (L.Browser.retina) ctx.scale(dpr, dpr);
                //     ctx.translate(padding.x, padding.y);

                //     for (let y = 0; y < Object.keys(capture_data).length; y++) {
                //         // draw
                //         var point = this._map.latLngToContainerPoint({
                //             lat: capture_data[y].geometry.coordinates[1],
                //             lng: capture_data[y].geometry.coordinates[0]
                //         });

                //         ctx.fillStyle = "yellow";
                //         ctx.fillRect(point.x, point.y, 3, 3);
                //     }

                // });

                // canvasLayer.addTo(map); 

                map.spin = false;
        }
    }

</script>

<style>

    .wrapper {
        display: inline-flex;
        max-height: 100vh;
        position: relative;
    }

    #map {
        height: 100vh;
        width: 75%;
    }

    .datatable-container {
        position: relative;
        margin-top: 1%;
        right: 0;
        height: 100%;
        width: 25%;
    }

    .datatable {
        padding: 0% 1% 1% 5%;
        position: relative;
        width: 100%;
        height: 100%;
    }

    .datatable th, td {
        border-right: thin solid black;
        border-bottom: thin solid black;
    }

    .datatable td {
        padding: 10px;
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
