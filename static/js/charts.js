let ageChart = document.getElementById('chart_age').getContext('2d');
let genderChart = document.getElementById('chart_gender').getContext('2d');
let expChart = document.getElementById('chart_experience').getContext('2d');
// console.log('hello', myChart);

var ages = $('#ages').data(ages);
var genders = $('#genders').data(genders);
var experience = $('#experience').data(experience);

console.log(experience.experience);

let colourPallette = ['#E1F5C4', '#EDE574', '#F9D423', '#FC913A', '#FF4E50', '#A7226E']

// F8B195   F67280   C06C84   6C5B7B   355C7D



// document.onreadystatechange = function () {
//     // if(document.readyState == 'complete'){
//     //     console.log(ages);
//     // }
//     console.log(document.readyState);
// }
let Chart1 = new Chart(chart_age, {
    type:'doughnut',
    data: {
        labels:['15 or under', '16-25', '26-35', '36-45', '46-55', '56-65', '65 or over'],
        datasets:[{
            label: 'Age range',
            data: ages.ages,
            backgroundColor: colourPallette,
            // backgroundColor: ['red', 'orange', 'yellow', 'green', 'blue', 'purple'],
        }],
        
    },
    options: {
        legend: {
            display: true,
            position: 'left'
        }
    }

});

let Chart2 = new Chart(chart_gender, {
    type:'doughnut',
    data: {
        labels:['Female', 'Male', 'Non-binary', 'Fluid', 'Other', 'N/A'],

        datasets:[{
            
            data: genders.genders,
            backgroundColor: colourPallette,
            // backgroundColor: ['red', 'orange', 'yellow', 'green', 'blue', 'purple'],
        }]
    },
    options:{}
});

let Chart3 = new Chart(chart_experience, {
    type:'doughnut',
    title: 'Experience',
    data: {
        labels:['None', 'A Little', 'Moderate', 'A Lot', 'Expert'],

        datasets:[{
            
            data: experience.experience,
            backgroundColor: colourPallette,
            // backgroundColor: ['red', 'orange', 'yellow', 'green', 'blue', 'purple'],
        }]
    },
    options:{}
});