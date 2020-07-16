Webcam.init();

Webcam.attach('#camera');

let imageFile = null;
let image = document.getElementById("image");
let cardText = document.getElementsByClassName("card-text")[0];
let card = document.getElementById("card");
let total = document.getElementById("total");
let tbody = document.getElementsByTagName("tbody")[0];

const products = {
    "colgate": {
        id: "00000121",
        price: "45"
    },
    "jbl": {
        id: "00000122",
        price: "60"
    }
}

let tableData = [];

card.style.display = "none";


function dataURLtoFile(dataurl, filename) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
}


function snapshot() {
    Webcam.snap((...n) => {
        image.src = n[0];
        imageFile = dataURLtoFile(n[0], 'image.jpg');
    })

}

function resetData() {
    tableData = [];
    tbody.innerHTML = `<tr>
                <td colspan="6" style="text-align: center;">No data</td>
              </tr>`;
    total.innerText = "";

}

function resetTable() {

    var totalValue = 0;
    var finalHTML = "";
    for (let i = 0; i < tableData.length; i++) {
        let item = tableData[i];
        finalHTML += `
            <tr>
                <td>${item["no"]}</td>
                <td>${item["id"]}</td>
                <td>${item["name"]}</td>
                <td>${item["quantity"]}</td>
                <td>${item["price"]}</td>
                <td>${item["quantity"] * parseInt(item["price"])}</td>
            </tr>
            `;

        totalValue += item["quantity"] * parseInt(item["price"]);
    }
    tbody.innerHTML = finalHTML;
    total.innerText = "Total: " + totalValue;

}


function insertData(data) {
    const product = (tableData.find(item => item.name == data));
    const productDetails = products[data];

    if (product) {
        product.quantity++;
    } else {
        tableData.push({
            no: tableData.length + 1,
            id: productDetails["id"],
            name: data,
            quantity: 1,
            price: productDetails["price"],
        })
    }

    resetTable();
}


function submit() {
    let formData = new FormData();
    formData.set("image", imageFile)
    fetch('./api/image_upload', {
        method: 'POST',
        body: formData
    })
        .then(r => r.json())
        .then(data => {
            console.log(data)
            insertData(data["product"])
        })
}
