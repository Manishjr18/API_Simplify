function checkQuestion() {
  let question = document.getElementById("question").value;

  fetch("/check_question", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question })
  })
  .then(res => res.json())
  .then(data => {
    let responseDiv = document.getElementById("response");
    let formDiv = document.getElementById("purchaseForm");

    if (data.related) {
      responseDiv.innerHTML = "<p style='color:green;'>" + data.message + "</p>";
      formDiv.style.display = "block";  // Show purchase form
    } else {
      responseDiv.innerHTML = "<p style='color:red;'>" + data.message + "</p>";
      formDiv.style.display = "none";   // Hide purchase form
    }
  });
}

let modalInstance;

document.addEventListener('DOMContentLoaded', function() {
  const modalElem = document.getElementById('successModal');
  modalInstance = M.Modal.init(modalElem, { dismissible: false });
});

const form = document.getElementById("purchaseForm");
const resultBox = document.getElementById("purchaseResult");
const purchaseBtn = document.getElementById("purchaseBtn");
const orderDetails = document.getElementById("orderDetails");
const doneBtn = document.getElementById("doneBtn");

form.addEventListener("submit", async function(e) {
  e.preventDefault();
  purchaseBtn.disabled = true;

  const user_name = document.getElementById("user_name").value.trim();
  const amount = document.getElementById("amount").value.trim();

  try {
    const res = await fetch("http://127.0.0.1:5000/purchase", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_name, amount })
    });

    const data = await res.json();

    if(res.ok){
      orderDetails.innerHTML = `Thank you <b>${user_name}</b>! <br> You successfully purchased <b>₹${amount}</b> worth of Digital Gold.`;

      modalInstance.open();

      // Done button closes modal immediately
      doneBtn.onclick = () => {
        modalInstance.close();
        purchaseBtn.disabled = false;
        form.reset();
      };

      // Automatic close after 15 seconds
      setTimeout(() => {
        if(modalInstance.isOpen) { // only close if still open
          modalInstance.close();
          purchaseBtn.disabled = false;
          form.reset();
        }
      }, 35000); // 15000ms = 15 seconds

    } else {
      resultBox.innerHTML = `<div class="card-panel red lighten-4">❌ ${data.message}</div>`;
      purchaseBtn.disabled = false;
    }

  } catch (err) {
    resultBox.innerHTML = `<div class="card-panel red lighten-4">⚠️ Something went wrong</div>`;
    purchaseBtn.disabled = false;
  }
});
