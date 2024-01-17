// alert('jssss')

        
$('.add-assessment').on('click', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        // url: '/assessment/add-assessment/',
        url: '',
        data: $("#assessment-form").serialize(),
        success: function (response) {
           
            console.log('Data:- ', response)
            //$('#assessment-form')[0].reset();
            $("#assessment-form").trigger("reset");
            $("#msg").text("form submitted successfully");
            $("#msg").show();
        },
        error: function (xhr) {
            console.log(xhr)
        }
    });
});