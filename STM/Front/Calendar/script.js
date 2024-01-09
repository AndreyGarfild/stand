$(document).ready(function() {
    var currentDate = new Date();

    // Loop through the next two years
    for (var i = 0; i < 730; i++) {
        var requestDate = new Date();
        requestDate.setDate(currentDate.getDate() + i);
        var month = requestDate.toLocaleString('default', { month: 'long' });
        var year = requestDate.getFullYear();
        var formattedDate = (requestDate.getDate() < 10 ? '0' : '') + requestDate.getDate() + '.' + (requestDate.getMonth() < 9 ? '0' : '') + (requestDate.getMonth() + 1) + '.' + year;

        // Make an AJAX request to the backend
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/statistics',
            data: JSON.stringify({ "date": formattedDate }),
            contentType: 'application/json',
            success: function(data) {
                // Update the UI with received statistics
                if (data.count > 0) {
                    var monthContainer = $('#' + month + '-' + year);
                    if (monthContainer.length === 0) {
                        // Create a new month container if it doesn't exist
                        $('#statistics-container').append('<div class="month-container" id="' + month + '-' + year + '"><div class="month-header">' + month + ' ' + year + '</div><ul class="statistics-list"></ul></div>');
                    }

                    // Append the statistics item to the corresponding month container
                    $('#' + month + '-' + year + ' .statistics-list').append('<li class="statistics-item">Date: ' + data.date + ', Count: ' + data.count + ', Sum: ' + data.summ + '</li>');
                }
            },
            error: function(xhr, status, error) {
                // Handle errors if any
                console.error('Error:', error);
            }
        });
    }
});
