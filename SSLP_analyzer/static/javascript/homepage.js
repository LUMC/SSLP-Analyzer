let sslp_value1 = document.getElementById("sslp_value1");
let sslp_value2 = document.getElementById("sslp_value2");
let sslp_value3 = document.getElementById("sslp_value3");
let sslp_value4 = document.getElementById("sslp_value4");
let population_dropdown = document.getElementById("SSLP-regio");



    for (let i = 0; i < options.length; i++) {
        let option = document.createElement("option");
        option.text = options[i];
        option.value = options[i];
        sslp_value1.appendChild(option);
    }

    for (let i = 0; i < options.length; i++) {
        let option = document.createElement("option");
        option.text = options[i];
        option.value = options[i];
        sslp_value2.appendChild(option);
    }

    for (let i = 0; i < options.length; i++) {
        let option = document.createElement("option");
        option.text = options[i];
        option.value = options[i];
        sslp_value3.appendChild(option);
    }

    for (let i = 0; i < options.length; i++) {
        let option = document.createElement("option");
        option.text = options[i];
        option.value = options[i];
        sslp_value4.appendChild(option);
    }

    for (let i = 0; i < populations.length; i++) {
        let population = document.createElement("option");
        population.text = populations[i];
        population.value = populations[i];
        population_dropdown.appendChild(population);
    }

    // Function to color the rows of the table based on the column 'Incidence(%)'
    function determineRB(d_perc) {
        if (d_perc > 30) {
            return 70;
        } else if (d_perc > 20) {
            return 90;
        } else if (d_perc > 10) {
            return 110;
        } else if (d_perc > 5) {
            return 130;
        } else if (d_perc > 3) {
            return 150;
        } else if (d_perc > 1) {
            return 170;
        } else if (d_perc > 0.1) {
            return 210;
        } else {
            return 255;
        }
    }

    function colorRows() {
        let table = document.getElementById('myTable');
        let rows = table.getElementsByTagName('tr');

        // Loop through each row starting at the second row (skipping the header)
        for (let i = 1; i < rows.length; i++) {
            let row = rows[i];
            let cells = row.getElementsByTagName('td');
            let probabilityCell = cells[cells.length - 3]; // Probability kolumn (Probability(%))

            let probability = parseFloat(probabilityCell.innerText);

            // Define the red and blue values based on the probability.
            let rb = determineRB(probability);

            // Alter the background color of the row.
            row.style.backgroundColor = 'rgb(' + rb + ', 255, ' + rb + ')';
        }
    }

    // Call the function when the window has finished loading.
    window.onload = function () {
        colorRows();
    };

    document.getElementById('ignore_button_upload').addEventListener('click', function () {
        let form = document.getElementById('button_form');
        form.setAttribute('novalidate', 'true');
    });

    document.getElementById('ignore_button_export').addEventListener('click', function () {
        let form = document.getElementById('button_form');
        form.setAttribute('novalidate', 'true');
    });