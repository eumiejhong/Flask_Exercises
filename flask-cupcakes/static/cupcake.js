const base_url = "http://127.0.0.1:5000";

function generateCupcakeHTML(cupcake) {
    return `
        <div data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button class="delete-button">Delete</button>
            </li>
            <img class="cupcake-img" src="${cupcake.image}" alt="(no image provided)">
        </div>
        `;
}

async function showCupcakes() {
    const response = await axios.get(`${base_url}/cupcakes`)
    .then(response=>response.data)
    .then(response=>console.log('Success:', response))
    for (let cupcake of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcake));
        $("#cupcakes-list").append(newCupcake);
    }
}

$("#new-cupcake-form").on("submit", async function(evt) {
    evt.preventDefault();
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const newCupcakeResponse = await axios.post(`${base_url}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeID = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${base_url}/cupcakes/${cupcakeID}`);
    $cupcake.remove();
});

$(showCupcakes);