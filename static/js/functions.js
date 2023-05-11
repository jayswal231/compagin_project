async function getData() {
  const data = await axios.get('http://127.0.0.1:8000/api/category/ethnicity/datalist/')
    .then(function (response) {
      return response.data
    })
    .catch(function (error) {
      return null
    });


  var newData = []
  var current_data = data.data
  current_data.forEach(element => {

    let newDataObj = {
      "category": element.category,
      "male": 0,
      "female": 0,
      "others": 0,
    }

    var obj = element.ethnicities
    var male_count = 0
    var female_count = 0
    var others_count = 0

    for (const key in obj) {
      male_count += obj[key].male
      female_count += obj[key].female
      others_count += obj[key].trans_sex
    }

    newDataObj.male = male_count
    newDataObj.female = female_count
    newDataObj.others = others_count

    newData.push(newDataObj)
  });

  var final_data = {
    "category": [],
    "male": [],
    "female": [],
    "others": []
  }

  newData.forEach(el => {
    final_data.category.push(el.category)
    final_data.male.push(el.male)
    final_data.female.push(el.female)
    final_data.others.push(el.others)
  })


  return final_data;

}




async function getAgeData() {
  const data = await axios.get('http://127.0.0.1:8000/api/age/ethnicity/datalist/')
    .then(function (response) {
      return response.data
    })
    .catch(function (error) {
      return null
    });


  var newData = []

  var current_data = data.data.ethnicity_data

  for (const key in current_data) {

    var newDataObj = {
      "ethnicity": key,
      "male": 0,
      "female": 0,
      "others": 0,
    }

    var male_count = 0
    var female_count = 0
    var others_count = 0

    var current_age_data = current_data[key]

    for (const age_key in current_age_data) {
      var current_temp_data = current_age_data[age_key]
      male_count += current_temp_data.male
      female_count += current_temp_data.female
      others_count += current_temp_data.trans_sex
    }

    newDataObj.male = male_count
    newDataObj.female = female_count
    newDataObj.others = others_count


    newData.push(newDataObj)


  }

  var final_data = {
    "ethnicity": [],
    "male": [],
    "female": [],
    "others": []
  }



  newData.forEach(el => {
    final_data.ethnicity.push(el.ethnicity)
    final_data.male.push(el.male)
    final_data.female.push(el.female)
    final_data.others.push(el.others)
  })

  // console.log(final_data)
  return final_data;



}





window.onload = async function () {

  var data = await getData();

  var ctx = document.getElementById("myChartCategory").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.category,
      datasets: [
        {
          label: "Male",
          data: data.male,
          backgroundColor: "red",
        },
        {
          label: "Female",
          data: data.female,
          backgroundColor: "blue"
        },
        {
          label: "Other",
          data: data.others,
          backgroundColor: "grey"
        }
      ]
    },
    options: {
      title: {
        text: "Bar Graph of Categories Data"
      },
      scales: {
        yAxes: [
          {
            interval: 1,
            ticks: {
              beginAtZero: true
            },

          }
        ]
      }
    }
  });



  // pie chart by cateory
  var totalByCategory = []
  for (var i = 0; i < data.male.length; i++) {

    total = data.male[i] + data.female[i] + data.others[i]
    totalByCategory.push(total)
  }




  var ctx = document.getElementById("myChartCategoryPie").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: data.category,
      datasets: [
        {
          label: "Total Participants",
          data: totalByCategory,
          backgroundColor: ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "black", "brown", "gray", "silver", "gold", "white"],
        }
      ]
    },
    options: {
      title: {
        text: "Pie Chart of Categories Data"
      },
      legend: {
        position: "right"
      }
    }
  });




  // bar chart by ethnicity
  var ageData = await getAgeData();


  var ctx = document.getElementById("myChartEthnicity").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ageData.ethnicity,
      datasets: [
        {
          label: "Male",
          data: ageData.male,
          backgroundColor: "red",
        },
        {
          label: "Female",
          data: ageData.female,
          backgroundColor: "blue"
        },
        {
          label: "Others",
          data: ageData.others,
          backgroundColor: "grey"
        }
      ]
    },
    options: {
      title: {
        text: "Bar Chart of Ethnicity Data"
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true
            }
          }
        ]
      }
    }
  });



  // ethnicity pie chart
  var totalByEthnicity = []
  for (var i = 0; i < ageData.male.length; i++) {
    total = ageData.male[i] + ageData.female[i] + ageData.others[i]
    totalByEthnicity.push(total)
  }


  var ctx = document.getElementById("myChartEthnicityPie").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ageData.ethnicity,
      datasets: [
        {
          label: "Total Participants",
          data: totalByEthnicity,
          backgroundColor: ["red", "orange", "yellow", "green", "blue"],
        }
      ]
    },
    options: {
      title: {
        text: "Pie Chart of Ethnicity Data"
      },
      legend: {
        position: "right"
      }
    }
  });



  // genderwise all data
  const maleData = ageData.male.reduce((accumulator, currentValue) => {
    return accumulator + currentValue;
  });

  const femaleData = ageData.female.reduce((accumulator, currentValue) => {
    return accumulator + currentValue;
  });

  const othersData = ageData.others.reduce((accumulator, currentValue) => {
    return accumulator + currentValue;
  });


  var ctx = document.getElementById("myChartGender").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Male", "Female", "Others"],
      datasets: [
        {
          label: "Number of Participants",
          data: [maleData, femaleData, othersData],
          backgroundColor: ["red", "blue", "green"]
        }
      ]
    },
    options: {
      title: {
        text: "Bar Chart"
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true
            }
          }
        ]
      }
    }
  });

  const totalParticipants = maleData + femaleData + othersData

  var malePercentage = maleData/totalParticipants * 100
  var femalePercentage = femaleData/totalParticipants * 100
  var othersPercentage = othersData/totalParticipants * 100

  var ctx = document.getElementById("myChart").getContext("2d");
    var myChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["Male", "Female", "Others"],
        datasets: [
          {
            label: "Percentage of Participants",
            data: [malePercentage, femalePercentage, othersPercentage],
            backgroundColor: ["red", "blue", "green"]
          }
        ]
      },
      options: {
        title: {
          text: "Pie Chart"
        }
      }
    });

  
}

