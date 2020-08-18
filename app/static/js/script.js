$(document).ready( function () {
    var table = $('#example').DataTable({
        "ajax": {
            "url": "/index_get_data",
            "dataType": "json",
            "dataSrc": "jobs",
            "contentType":"application/json"
        },
        "columns": [
            {"data": "job_title"},
            {"data": "company"},
            {"data": "city"},
            {"data": "date"},
            {"data": "job_description"},
            {"data": "url"},
        ]
    });
    setInterval( function () {
        table.ajax.reload( null, false ); // user paging is not reset on reload
    }, 30000 );
} );