let haplo_row_clone

document.addEventListener("DOMContentLoaded", function() {    
    const haplotable = document.getElementById("haplotable");
    const haplo_row = haplotable.rows[haplotable.rows.length - 1];
    const haplo_inputs = haplo_row.querySelectorAll("input");
    haplo_inputs.forEach(el => el.addEventListener('input', add_inputs));
    haplo_row_clone = haplo_row.cloneNode(true);


});
  

// console.log(table.rows.length)

function add_inputs(el) {
    let haplo_row_new = haplo_row_clone.cloneNode(true)
    
    const haplotable = document.getElementById("haplotable");
    const haplo_row = haplotable.rows[haplotable.rows.length - 1];
    const haplo_inputs = haplo_row.querySelectorAll("input");
    let edits = false;
    for (const inp in haplo_inputs) {
        if (Object.hasOwnProperty.call(haplo_inputs, inp)) {
            const inp_el = haplo_inputs[inp];
            if (inp_el.value != "") {
                edits =true
            }
        }
    }
    
    if (edits) {

        haplo_row_new.querySelectorAll("input").forEach(el => el.addEventListener('input', add_inputs));
        haplotable.appendChild(haplo_row_new)
    }
}
