(function($) {
    $(document).ready(function() {
        $('#id_batch').change(function() {
            var batchId = $(this).val();
            if (!batchId) {
                $('#id_student').empty();  // Clear student dropdown if no batch is selected
                return;
            }

            $.ajax({
                url: '/admin/course/get_students/',  // This should be the URL for the Ajax request to get students
                data: {
                    'batch_id': batchId
                },
                success: function(data) {
                    var studentSelect = $('#id_student');
                    studentSelect.empty();  // Clear current options
                    $.each(data.students, function(index, student) {
                        studentSelect.append(new Option(student.name, student.id));
                    });
                }
            });
        });
    });
})(django.jQuery);

