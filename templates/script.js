let modalInstance;

document.addEventListener('DOMContentLoaded', function() {
  // Modal initialize with dismissible:false (cannot close by clicking outside)
  const modalElem = document.getElementById('successModal');
  modalInstance = M.Modal.init(modalElem, { dismissible: false });
});

const form = document.getElementById("purchaseForm");
const resultBox = document.getElementById("purchaseResult");
const purchaseBtn = document.getElementById("purchaseBtn");
const orderDetails = document.getElementById("orderDetails");

form.addEventListener("submit", async function(e){
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
      orderDetails.innerHTML =
        `Thank you <b>${user_name}</b>! <br> You successfully purchased <b>₹${amount}</b> worth of Digital Gold.`;

      modalInstance.open(); // open popup

      // Done button closes modal and resets form
      const doneBtn = document.getElementById("doneBtn");
      doneBtn.onclick = () => {
        modalInstance.close();
        purchaseBtn.disabled = false;
        form.reset();
      };

    } else {
      resultBox.innerHTML =
        `<div class="card-panel red lighten-4">❌ ${data.message}</div>`;
      purchaseBtn.disabled = false;
    }

  } catch (err) {
    resultBox.innerHTML =
      `<div class="card-panel red lighten-4">⚠️ Something went wrong</div>`;
    purchaseBtn.disabled = false;
  }
});
