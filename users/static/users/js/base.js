
// courses show carousal js start 

var myCarousel = document.querySelector('#myCarousel')
var carousel = new bootstrap.Carousel(myCarousel, {
  interval: 100000
})

$('.carousel .carousel-item').each(function(){
    var minPerSlide = 4;
    var next = $(this).next();
    if (!next.length) {
    next = $(this).siblings(':first');
    }
    next.children(':first-child').clone().appendTo($(this));
    
    for (var i=0;i<minPerSlide;i++) {
        next=next.next();
        if (!next.length) {
            next = $(this).siblings(':first');
        }
        
        next.children(':first-child').clone().appendTo($(this));
      }
});

// courses shown carousal js end

// rating js for css start

let stars =  document.getElementsByClassName("star"); 
let output =  document.getElementById("output"); 

// Funtion to update rating 
function gfg(n) { 
    remove(); 
    for (let i = 0; i < n; i++) { 
        if (n == 1) cls = "one"; 
        else if (n == 2) cls = "two"; 
        else if (n == 3) cls = "three"; 
        else if (n == 4) cls = "four"; 
        else if (n == 5) cls = "five"; 
        stars[i].className = "star " + cls; 
    } 
    output.innerText = "Rating is: " + n + "/5"; 
    $('#rating').val(n)
    $('#rating-form').submit()
} 

// To remove the pre-applied styling 
function remove() { 
    let i = 0; 
    while (i < 5) { 
        stars[i].className = "star"; 
        i++; 
    } 
}

// rating js for css end


// $('#courseid').onClick(function (e) {
//   e.preventDefault();

//   $.ajax({
//     type: "GET",
//     url: "{% url 'showcourses' %}",
//     success:function(response){ 
//       alert('showed'); 
//     },
//     error: function(response){
//       alert('error');
//     },
//   }) 
// });