var numCount = document.getElementById('num_count');
var plusBtn = document.getElementById('button_plus');
var minusBtn = document.getElementById('button_minus');
plusBtn.onclick = function() {
  var qty = parseInt(numCount.value);
  qty = qty + 1;
  numCount.value = qty;
}
minusBtn.onclick = function() {
  var qty = parseInt(numCount.value);
      if (qty>1){
  qty = qty - 1;
  numCount.value = qty;
  }
}


$(document).ready(function() {
  $(".quiz1").hide();
      $('input[type="radio"]').click(function() {
        if ($(this).attr("value") == "two_y") {
          $(".quiz1").show();
          $(".quiz2").hide();
          $('#form_cart').push();
        }
        if ($(this).attr("value") == "one_y") {
          $(".quiz1").hide();
          $(".quiz2").show();
          $('#form_cart').sisyphus();
        }
      });
  });