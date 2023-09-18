var numCount = document.getElementById('num_count_product');
var plusBtn = document.getElementById('button_plus_product');
var minusBtn = document.getElementById('button_minus_product');
var basket_products = document.querySelectorAll('.basket_product');
var login_errors = document.querySelector("body > div.fdwn > div > div > form > div.login_errors > ul > li");
// login_errors.value = login_errors.substr(5);
if(plusBtn != null && minusBtn != null ) {
  plusBtn.onclick = function () {
    var qty = parseInt(numCount.value);
    qty = qty + 1;
    numCount.value = qty;
  }
  minusBtn.onclick = function () {
    var qty = parseInt(numCount.value);
    if (qty > 1) {
      qty = qty - 1;
      numCount.value = qty;
    }
  }
}
basket_products.forEach(function(element) {
        let num_count = element.querySelector("#num_count");
        let button_minus = element.querySelector("#button_minus");
        let button_plus = element.querySelector("#button_plus");
        button_plus.addEventListener(
            'click',
            (e) =>{
                let qty = parseInt(num_count.value);
                qty = qty + 1;
                num_count.value = qty;
            }
        )
        button_minus.addEventListener(
            'click',
            (e) =>{
                let qty = parseInt(num_count.value);
                if (qty > 1) {
                  qty = qty - 1;
                  num_count.value = qty;
                }
            }
        )
      });














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


// document.querySelector('#main').addEventListener(
//   'change',
//   (e) => {
//     const checked = e.target.checked;
//     console.log(e.target);
//     document.querySelectorAll('.check').forEach(
//       (el) => {
//         el.checked = checked;
//       },
//     );
//   }
// );
    const checkboxes = document.querySelectorAll('.check');
    const select_all = document.querySelector('.select_all');
    const cancel_all = document.querySelector('.cancel_all');



select_all.addEventListener(
  'click',
  (e) => {
    checkboxes.forEach(function(element) {
      element.checked=true;
    });
  }
)
cancel_all.addEventListener(
  'click',
  (e) => {
    checkboxes.forEach(function(element) {
      element.checked=false;
    });
  }
)
