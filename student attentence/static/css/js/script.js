
// Attendance Management System

console.log("Attendance System Loaded");

// Confirm before deleting
function deleteConfirm() {

    return confirm("Are you sure you want to delete this record?");

}

// Search Student
function searchStudent() {

    let input = document.getElementById("search").value.toUpperCase();

    let table = document.getElementById("studentTable");

    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {

        let td = tr[i].getElementsByTagName("td")[1];

        if (td) {

            let txt = td.textContent || td.innerText;

            if (txt.toUpperCase().indexOf(input) > -1) {

                tr[i].style.display = "";

            } else {

                tr[i].style.display = "none";

            }

        }

    }

}

// Current Date
window.onload = function () {

    let today = new Date();

    let date = today.toLocaleDateString();

    let element = document.getElementById("currentDate");

    if (element) {

        element.innerHTML = date;

    }

}

// Attendance Percentage
function attendancePercentage(total, present) {

    if (total == 0)

        return 0;

    return ((present / total) * 100).toFixed(2);

}