
// const hierarchy = {
//     "provinces": {
//         "Province 1": {
//             "districts": {
//                 "Bhojpur": {
//                     "palikas": [
//                         "Bhojpur",
//                         "Salpa Silichho"
//                     ]
//                 },
//                 "Dhankuta": {
//                     "palikas": [
//                         "Dhankuta",
//                         "Chhathar Jorpati"
//                     ]
//                 },
//                 "Ilam": {
//                     "palikas": [
//                         "Mai Municipality",
//                         "Chulachuli",
//                         "Fakfokthum"
//                     ]
//                 }
//             }
//         },
//         "Province 2": {
//             "districts": {
//                 "Bara": {
//                     "palikas": [
//                         "Kalaiya",
//                         "Simraungadh",
//                         "Nijgadh"
//                     ]
//                 },
//                 "Parsa": {
//                     "palikas": [
//                         "Birgunj",
//                         "Thori",
//                         "Jirabhawani",
//                         "Chhipaharmai",
//                         "Sakhuwa Prasauni"
//                     ]
//                 }
//             }
//         },
//         "Bagmati Province": {
//             "districts": {
//                 "Kathmandu": {
//                     "palikas": [
//                         "Kathmandu",
//                         "Kageshwari-Manohara",
//                         "Budhanilkantha",
//                         "Dakshinkali",
//                         "Gokarneshwor",
//                         "Nagarjun",
//                         "Shankharapur",
//                         "Tarakeshwar"
//                     ]
//                 },
//                 "Lalitpur": {
//                     "palikas": [
//                         "Lalitpur",
//                         "Godawari",
//                         "Mahalaxmi"
//                     ]
//                 },
//                 "Bhaktapur": {
//                     "palikas": [
//                         "Bhaktapur",
//                         "Changunarayan",
//                         "Madhyapur Thimi"
//                     ]
//                 }
//             }
//         }
//     }
// };


// window.onload = function () {
//     // Get references to the select elements
//     const provinceSelect = document.getElementById("province-select");
//     const districtSelect = document.getElementById("district-select");
//     const palikaSelect = document.getElementById("palika-select");

//     // Add event listeners to each select element
//     provinceSelect.addEventListener("change", updateDistrictSelect);
//     districtSelect.addEventListener("change", updatePalikaSelect);

//     // Populate the province select element
//     for (const province in hierarchy.provinces) {
//         const option = document.createElement("option");
//         option.text = province;
//         provinceSelect.add(option);
//     }

//     // Update the district select element based on the selected province
//     function updateDistrictSelect() {
//         // Clear the district and palika select elements
//         districtSelect.innerHTML = "<option value=''>Select a district</option>";
//         palikaSelect.innerHTML = "<option value=''>Select a palika</option>";

//         // Get the selected province
//         const selectedProvince = provinceSelect.value;

//         // Populate the district select element with the districts in the selected province
//         for (const district in hierarchy.provinces[selectedProvince].districts) {
//             const option = document.createElement("option");
//             option.text = district;
//             districtSelect.add(option);
//         }
//     }

//     // Update the palika select element based on the selected district
//     function updatePalikaSelect() {
//         // Clear the palika select element
//         palikaSelect.innerHTML = "<option value=''>Select a palika</option>";

//         // Get the selected province and district
//         const selectedProvince = provinceSelect.value;
//         const selectedDistrict = districtSelect.value;

//         // Populate the palika select element with the palikas in the selected district
//         for (const palika of hierarchy.provinces[selectedProvince].districts[selectedDistrict].palikas) {
//             const option = document.createElement("option");
//             option.text = palika;
//             palikaSelect.add(option);
//         }
//     }
// };





// const activity = [
//     { "code": "1.1.3", "name": "Condution of health campaign" },
//     { "code": "1.2.3", "name": "Condution of awareness campaign" },
//     { "code": "2.1.1", "name": "Training for teachers" },
//     { "code": "2.1.2", "name": "Construction of school buildings" },
//     { "code": "2.1.3", "name": "Distribution of school supplies" },
//     { "code": "2.2.1", "name": "Training for farmers" },
//     { "code": "2.2.2", "name": "Distribution of agricultural inputs" },
//     { "code": "2.2.3", "name": "Establishment of farmer cooperatives" },
//     { "code": "3.1.1", "name": "Construction of roads" },
//     { "code": "3.1.2", "name": "Rehabilitation of bridges" },
//     { "code": "3.2.1", "name": "Provision of clean water supply" },
//     { "code": "3.2.2", "name": "Construction of public toilets" },
//     { "code": "3.2.3", "name": "Installation of water pumps" },
//     { "code": "4.1.1", "name": "Support for small businesses" },
//     { "code": "4.1.2", "name": "Training for entrepreneurs" },
//     { "code": "4.2.1", "name": "Construction of community centers" },
//     { "code": "4.2.2", "name": "Training for community leaders" },
//     { "code": "4.2.3", "name": "Provision of public services" },
//     { "code": "5.1.1", "name": "Awareness campaign on environmental protection" },
//     { "code": "5.1.2", "name": "Promotion of renewable energy sources" },
//     { "code": "5.2.1", "name": "Disaster risk reduction training" },
//     { "code": "5.2.2", "name": "Construction of emergency shelters" },
//     { "code": "5.2.3", "name": "Provision of emergency supplies" }
// ];


// const activitySelect = document.getElementById('activity');
// const activityNameInput = document.getElementById('activity-name');

// activity.forEach((act) => {
//     const option = document.createElement('option');
//     option.value = act.code;
//     option.textContent = act.code;
//     activitySelect.appendChild(option);
// });

// activitySelect.addEventListener('change', (e) => {
//     const selectedCode = e.target.value;
//     const selectedActivity = activity.find((act) => act.code === selectedCode);
//     activityNameInput.value = selectedActivity ? selectedActivity.name : '';
// });
