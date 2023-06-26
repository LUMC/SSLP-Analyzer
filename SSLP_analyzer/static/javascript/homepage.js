var waarde1 = document.getElementById("SSLP-waarde1");
    var waarde2 = document.getElementById("SSLP-waarde2");
    var waarde3 = document.getElementById("SSLP-waarde3");
    var waarde4 = document.getElementById("SSLP-waarde4");
    var population_dropdown = document.getElementById("SSLP-regio");



    for (var i = 0; i < options.length; i++) {
        var option = document.createElement("option");
        option.text = options[i];
        option.value = options[i];
        waarde1.appendChild(option);
    }

    for (var i = 0; i < options.length; i++) {
        var option = document.createElement("option");
        option.text = options[i];
        option.value = options[i];
        waarde2.appendChild(option);
    }

    for (var i = 0; i < options.length; i++) {
        var option = document.createElement("option");
        option.text = options[i];
        option.value = options[i];
        waarde3.appendChild(option);
    }

    for (var i = 0; i < options.length; i++) {
        var option = document.createElement("option");
        option.text = options[i];
        option.value = options[i];
        waarde4.appendChild(option);
    }

    for (var i = 0; i < populations.length; i++) {
        var population = document.createElement("option");
        population.text = populations[i];
        population.value = populations[i];
        population_dropdown.appendChild(population);
    }

    // Functie om de tabelrijen te kleuren op basis van de kolom 'Incidence(%)'
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
        var table = document.getElementById('myTable');
        var rows = table.getElementsByTagName('tr');

        // Loop door elke rij, beginnend bij de tweede rij (overslaan van de kop)
        for (var i = 1; i < rows.length; i++) {
            var row = rows[i];
            var cells = row.getElementsByTagName('td');
            var probabilityCell = cells[cells.length - 3]; // Voorlaatste cel in de rij (Probability(%))

            var probability = parseFloat(probabilityCell.innerText);

            // Bepaal de waarde voor rood en blauw op basis van de probability
            var rb = determineRB(probability);

            // Pas de achtergrondkleur en tekstkleur van de rij aan
            row.style.backgroundColor = 'rgb(' + rb + ', 255, ' + rb + ')';
        }
    }

    // Roept de functie aan wanneer het document is geladen
    window.onload = function () {
        colorRows();
    };

    document.getElementById('ignore_button_upload').addEventListener('click', function () {
        var form = document.getElementById('button_form');
        form.setAttribute('novalidate', 'true');
    });

    document.getElementById('ignore_button_export').addEventListener('click', function () {
        var form = document.getElementById('button_form');
        form.setAttribute('novalidate', 'true');
    });