<template>
  <div id="map">
  </div>
</template>

<script>

    import axios from 'axios';

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
            }).setView([41.31, 69.28], 16);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
            }).addTo(map);
            // Variable for saving single layer data
            var layer;
            
            // Variable for saving all layers data
            var allLayers;
            
            // Variable for saving popup content
            var popupContent;
            
            // Variable for saving area data
            var area;
            
            // Variable for saving polygon data
            var polygon;
            
            // Variable for saving geometry data
            var geometry;
            
            // Variable for saving DrawControl data
            var drawControl;
            
            // Variable for saving options for DrawControl
            var drawOptions;
            
            // Variable for saving latitude & longitute data
            var latlngs;
            var Layer;
            
            // Variable for preventing new layers from clicking
            var layerClickPrevent = false;
            
            // Variable for checking status of delete operations
            var deleteStartStatus = false;
            
            // Variable for checking status of edit operations
            var editStartStatus = false;
            
            // Variable for saving data to
            var data
            
            // Creating a FeatureGroup for drawn items & adding it to map
            var drawnItems = new L.FeatureGroup();
            map.addLayer(drawnItems);

            // Creating a FeatureGroup for edited items & adding it to map
            var editItems = new L.FeatureGroup();
            map.addLayer(editItems);

            // Function for defining options for DrawControl
            const defineDrawOptions = (options) => {
                drawOptions = {
                    position: 'topright',
                    draw: options.can_draw ? {
                    polygon: {
                        allowIntersection: false, // Restricts shapes to simple polygons
                        drawError: {
                            color: 'red', // Color the shape will turn when intersects
                            message: 'Lines should not intersect', // Message that will show when intersect
                        },
                        shapeOptions: {
                            color: '#50b8e7',
                        }
                    },
                    circle: false,
                    circlemarker: false,
                    marker: false,
                    polyline: false,
                    rectangle: false,
                    } : false,
                    edit: options.can_edit ? {
                    featureGroup: options.operatingLayer,
                    remove: options.can_delete ? true : false,
                    } : false,
                }
            }

            // Function for loading DrawControl (idk why I called it reload, bc it both load and reloads the DrawControl)
            const reloadDrawControl = (events, options) => {
                if (events === 'initial') {
                    defineDrawOptions(options);
                    drawControl = new L.Control.Draw(drawOptions);
                    map.addControl(drawControl);
                } else if (events === 'secondary') {
                    map.removeControl(drawControl);
                    defineDrawOptions(options);
                    drawControl = new L.Control.Draw(drawOptions);
                    map.addControl(drawControl);
                }
            }

            // Function for area calculation
            const findArea = (layer, events) => {
                if (events === 'created') {
                    var objects = layer.getLatLngs()[0];
                    geometry = [[]];
                    var first = "";
                    for (var i = 0; i < objects.length; i++) {
                        if (i == 0) {
                            first = new L.latLng(objects[i].lat, objects[i].lng)
                        };

                        var latlng = new L.latLng(objects[i].lat, objects[i].lng);
                        var point = latlng;

                        geometry[0].push([point['lng'], point['lat']]);
                    }
                    geometry[0].push([first['lng'], first['lat']]);

                    polygon = turf.polygon(geometry);
                    area = turf.area(polygon) / 10000;
                } else if (events === 'edited') {
                    var objects = layer.getLatLngs()[0];
                    geometry = [[]];
                    var first = "";
                    for (var i = 0; i < objects.length; i++) {
                        if (i == 0) {
                            first = new L.latLng(objects[i].lat, objects[i].lng)
                        };

                        var latlng = new L.latLng(objects[i].lat, objects[i].lng);
                        var point = latlng;

                        geometry[0].push([point['lng'], point['lat']]);
                    }
                    geometry[0].push([first['lng'], first['lat']]);

                    polygon = turf.polygon(geometry);

                    layer.feature.geometry = geometry;
                    layer.feature.properties.area = turf.area(polygon) / 10000;
                }
            }

            // Function for loading popups
            const loadPopup = (events, layer) => {
            
                if (events === 'created') {
                    popupContent = `
                    <div id="popup-content">
                        <table id="created-table">
                            <tr>
                                <td><label for="name" class="label-name"></label><span class="content-name">Name</span></td>
                                <td><input name="name" type="text" required></td>
                            </tr>
                            <tr>
                                <td><label for="area" class="label-name"></label><span class="content-name">Area (ha)</span></td>
                                <td><input name="area" type="number" value="${area.toFixed(2)}" required disabled></td>
                            </tr>
                            <tr>
                                <td><label for="description"></label><span class="content-name">Description</span></td>
                                <td><input name="description" type="text" required></td>
                            </tr>
                        </table>
                        <div id="save-layer">
                            <button id="save-button">save</button>
                            <button id="cancel-button">cancel</button>
                        </div>
                    </div>
                    `;

                    layer.bindPopup(popupContent).openPopup();

                    $('#cancel-button').click(() => {
                        drawnItems.clearLayers();
                    });

                    $('#save-button').click(() => {
                        data = polygon;
                        data.properties = {
                            'name': $('input[name="name"]').val(),
                            'area': $('input[name="area"]').val(),
                            'description': $('input[name="description"]').val()
                        }
                        if (data.properties['name'] != null && 
                            data.properties['name'].length != 0 && 
                            data.properties['area'] != null && 
                            data.properties['area'].length != 0 && 
                            data.properties['description'] != null &&
                            data.properties['description'].length != 0) {
                                // console.log(data);
                                createBuilding(data);
                                layer.closePopup();
                        } else {
                            fireAlert('Please, fill in all the fields!', 'error');
                        }
                        
                    });

                } else if (events === 'generated') {
                    data = layer.feature.properties;
                    return popupContent = `
                        <div id="popup-content">
                            <table id="generated-table">
                                <tr>
                                    <td>Name</td>
                                    <td>${data.name}</td>
                                </tr>
                                <tr>
                                    <td>Area</td>
                                    <td>${data.area}</td>
                                </tr>
                                <tr>
                                    <td>Description</td>
                                    <td>${data.description}</td>
                                </tr>
                            </table>
                        </div>
                    `;
                } else if (events === 'edited') {

                    data = layer.feature;
                    var id = data.id;

                    layer.unbindPopup();

                    popupContent = `
                    <div id="popup-content">
                        <table id="created-table">
                            <tr>
                                <td><label for="name" class="label-name"></label><span class="content-name">Name</span></td>
                                <td><input name="name" type="text" value="${data.properties.name}" required></td>
                            </tr>
                            <tr>
                                <td><label for="area" class="label-name"></label><span class="content-name">Area (ha)</span></td>
                                <td><input name="area" type="number" value="${data.properties.area.toFixed(2)}" required disabled></td>
                            </tr>
                            <tr>
                                <td><label for="description"></label><span class="content-name">Description</span></td>
                                <td><input name="description" type="text" value="${data.properties.description}" required></td>
                            </tr>
                        </table>
                        <div id="save-layer">
                            <button id="save-button">save</button>
                            <button id="cancel-button">cancel</button>
                        </div>
                    </div>
                    `;
                    layer.bindPopup(popupContent).openPopup();

                    $('.leaflet-popup-close-button').click((e) => {
                        layer.closePopup();
                    })

                    $('#cancel-button').click((e) => {
                        editItems.clearLayers();
                        var options = {
                            can_draw: true, 
                            can_edit: true, 
                            can_delete: true,
                            operatingLayer: drawnItems,
                        }
                        reloadDrawControl('secondary', options);
                        getAllBuildings();
                    });

                    $('#save-button').click(() => {
                        data = polygon;
                        data.properties = {
                            'name': $('input[name="name"]').val(),
                            'area': $('input[name="area"]').val(),
                            'description': $('input[name="description"]').val(),
                        }
                        if (data.properties['name'] != null && 
                            data.properties['name'].length != 0 && 
                            data.properties['area'] != null && 
                            data.properties['area'].length != 0 && 
                            data.properties['description'] != null &&
                            data.properties['description'].length != 0) {
                                console.log(polygon);
                                updateBuilding(data, id);
                                layer.closePopup();
                        } else {
                            fireAlert('Please, fill in all the fields!', 'error');
                        }
                    });
                }

            }

            // Function for firing alerts
            const fireAlert = (message, icon) => {
                Swal.fire({
                    icon: icon,
                    title: message,
                    showConfirmButton: false,
                    timer: 1500
                })
            }

            // Getting all buildnigs from DB and diplaying them on map
            const getAllBuildings = () => {
            
                axios.get('/get-all-buildings')
                .then(function (response) {
                    var states = {
                        features: [],
                        type: "FeatureCollection"
                    }
                    allLayers = response.data;
                    for (var i in Object.keys(allLayers)) {
                        layer = allLayers[i];
                        var state = {
                            "type": "Feature",
                            "properties": layer.properties,
                            "geometry": layer.geometry
                        }
                        state.id = layer._id;
                        states.features.push(state);
                    }
                    Layer = L.geoJSON(states, {
                        onEachFeature: function (feature, layer) {
                            layer.setStyle({
                                color: '#42C2FF'
                            });
                                layer.on('click', (e) => {
                                    if (layerClickPrevent === true) {
                                        // UPDATE CODE HERE
                                    } else {
                                        if (deleteStartStatus === 'true') {
                                            // PDATE CODE HERE TOO
                                        } else {
                                            editItems.clearLayers();
                                            layerClickPrevent = true;
                                            editItems.addLayer(layer);
                                            var options = {
                                                can_draw: false, 
                                                can_edit: true, 
                                                can_delete: true,
                                                operatingLayer: editItems,
                                            }
                                            reloadDrawControl('secondary', options);
                                        }
                                    }
                                    $('.leaflet-popup-close-button').click((e) => {
                                        layerClickPrevent = false;
                                        editItems.clearLayers();
                                        getAllBuildings();
                                        var options = {
                                            can_draw: true, 
                                            can_edit: true, 
                                            can_delete: true,
                                            operatingLayer: drawnItems,
                                        }
                                        reloadDrawControl('secondary', options);
                                    })
                                });
                        }
                    }).bindPopup(function (layer) {
                        return popupContent = loadPopup('generated', layer);
                    }).addTo(map);
                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                });
            };
            
            // Defining options for DrawControl
            var options = {
                can_draw: true, 
                can_edit: true, 
                can_delete: true,
                operatingLayer: drawnItems,
            }

            reloadDrawControl('initial', options);
            getAllBuildings();

            // Wrapper function for axios method of creating buildings
            const createBuilding = (data) => {
                axios.post('/add-building', data)
                .then(function (response) {
                    // handle success
                    fireAlert('Building created successfully!', 'success');
                    drawnItems.clearLayers();
                    getAllBuildings();
                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                    fireAlert('Some thing went wrong while creating the buliding!', 'error');
                });
            }

            // Wrapper function for axios method of updating buildings
            const updateBuilding = (data, id) => {
                axios.post('/update-building/' + id, data)
                .then(function (response) {
                    // handle success
                    fireAlert('Building updated successfully!', 'success');
                    drawnItems.clearLayers();
                    getAllBuildings();
                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                    fireAlert('Some thing went wrong while updating the building!', 'error');
                });
            }

            const deleteBuilding = (id) => {
                axios.post('/delete-building/' + id)
                .then(function (response) {
                    // handle success
                    fireAlert('Building deleted successfully!', 'success');
                    drawnItems.clearLayers();
                    getAllBuildings();
                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                    fireAlert('Some thing went wrong while deleting the building!', 'error');
                });
            }

            // const editBuildingStop = () => {
                // layerClickPrevent = false;
                // Layer.clearLayers();
                // editItems.clearLayers();
                // getAllBuildings();
                // var options = {
                //     can_draw: true, 
                //     can_edit: true, 
                //     can_delete: true,
                //     operatingLayer: drawnItems,
                // }
                // reloadDrawControl('secondary', options);
            // }

            // Map event for creating layers
            map.on("draw:created", (e) => {

                var options = {
                    can_draw: false, 
                    can_edit: true, 
                    can_delete: true,
                    operatingLayer: drawnItems,
                }
                reloadDrawControl('secondary', options);

                layer = e.layer;
                drawnItems.addLayer(layer);

                findArea(layer, 'created');
                loadPopup('created', layer);
            
            });
            
            // Map event for editing layers
            map.on("draw:edited", (e) => {
                
                e.layers._layers = Object.values(editItems._layers);
                layer = Object.values(editItems._layers)[0];
                findArea(layer, 'edited');
                loadPopup('edited', layer);
            
            });
            
            // Map event for editing stopped
            // map.on("draw:editstop", (e) => {
            //     editBuildingStop(e);
            // })

            // Map event for starting deleting layers
            // map.on("draw:deletestart", (e) => {

            //     deleteStartStatus = true;

            //     // var options = {
            //     //     can_draw: true, 
            //     //     can_edit: true, 
            //     //     can_delete: true,
            //     //     operatingLayer: drawnItems,
            //     // }
            //     // reloadDrawControl('secondary', options);

            // });
            
            // Map event for deleting layers
            map.on("draw:deleted", (e) => {

                var id = Object.values(e.layers._layers)[0].feature.id;
                deleteBuilding(id);

            });

        }
    }

</script>

<style scoped>

</style>
