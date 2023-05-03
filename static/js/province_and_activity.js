async function getActivities() {
    const data = await axios.get('http://127.0.0.1:8000/activities/')
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            return null
        });

    return data;
}


async function getAllProvinceData() {
    const data = await axios.get('http://127.0.0.1:8000/datalist/')
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            return null
        });

    return data;
}






window.onload = async function () {


    const activity = await getActivities();

    // const currentActivityCode = document.getElementById('current_activity_code');
    // const currenActivityName = document.getElementById('current_activity_name');

    // if (currentActivityCode == null) {
    //     console.log("In Other Pages")
    // } else {
    //     console.log("In the Participant Data Entry Page")
    // }

    if (activity != null) {

        const activitySelect = document.getElementById('activity');
        const activityNameInput = document.getElementById('activity-name');

        activity.forEach((act) => {
            const option = document.createElement('option');
            option.value = act.code;
            option.textContent = act.code;


            // setting the option to the selected if the option is found
            // if (currentActivityCode != null && currentActivityCode.textContent == act.code) {
            //     option.selected = true
            // }

            activitySelect.appendChild(option);
        });

        activitySelect.addEventListener('change', (e) => {
            const selectedCode = e.target.value;
            const selectedActivity = activity.find((act) => act.code === selectedCode);
            activityNameInput.value = selectedActivity ? selectedActivity.name : '';
        });


        // // setting the data send from the server to the activity name, start date and end date
        // if (currentActivityCode != null) {
        //     activityNameInput.value = currenActivityName.textContent
        

        // }

    }




    const hierarchy = await getAllProvinceData();


    // Get references to the select elements
    const provinceSelect = document.getElementById("province-select");
    const districtSelect = document.getElementById("district-select");
    const palikaSelect = document.getElementById("palika-select");

    // Add event listeners to each select element
    provinceSelect.addEventListener("change", updateDistrictSelect);
    districtSelect.addEventListener("change", updatePalikaSelect);

    // Populate the province select element
    for (const province in hierarchy.provinces) {
        const option = document.createElement("option");
        option.text = province;
        provinceSelect.add(option);
    }

    // Update the district select element based on the selected province
    function updateDistrictSelect() {
        // Clear the district and palika select elements
        districtSelect.innerHTML = "<option value=''>Select a district</option>";
        palikaSelect.innerHTML = "<option value=''>Select a palika</option>";

        // Get the selected province
        const selectedProvince = provinceSelect.value;

        // Populate the district select element with the districts in the selected province
        for (const district in hierarchy.provinces[selectedProvince].districts) {
            const option = document.createElement("option");
            option.text = district;
            districtSelect.add(option);
        }
    }

    // Update the palika select element based on the selected district
    function updatePalikaSelect() {
        // Clear the palika select element
        palikaSelect.innerHTML = "<option value=''>Select a palika</option>";

        // Get the selected province and district
        const selectedProvince = provinceSelect.value;
        const selectedDistrict = districtSelect.value;

        // Populate the palika select element with the palikas in the selected district
        for (const palika of hierarchy.provinces[selectedProvince].districts[selectedDistrict].palikas) {
            const option = document.createElement("option");
            option.text = palika;
            palikaSelect.add(option);
        }
    }
};









