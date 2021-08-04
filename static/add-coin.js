/** processForm: get data from form and make AJAX call to our API. */

async function processForm(evt) {
    evt.preventDefault()
    let body = {
        name: evt.target[0].value,
        value: evt.target[1].value,
    }

    await axios({
        method: 'post',
        url: '/api/coins',
        data: body
    })
    .then(response => {
        handleResponse(response)
    })
    .catch(error => {
        console.log("error: ", error)
    })

}

/** handleResponse: deal with response from our coin API. */

function handleResponse(resp) {
    const errorBoxes = document.getElementsByTagName('B')
    Array.from(errorBoxes).map(box => box.innerText = '')

    if (resp.data.error) {
        let errorKeys = Object.keys(resp.data.error)
        errorKeys.map(errorName => {
            let bBox = document.getElementById(`${errorName}-err`)
            bBox.innerText = resp.data.error[errorName]
        })
    } else { }
}


const coinForm = document.getElementById("add-coin-form")
coinForm.addEventListener("submit", processForm)
