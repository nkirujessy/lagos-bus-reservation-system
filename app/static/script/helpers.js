const pathname =  window.location.pathname.split(`/`).reverse()[0]
const formSerialize = (formselector) => {
    let myform = document.querySelector(formselector),
        forment = new FormData(myform).entries()

    return Object.assign(...Array.from(forment, ([x, y]) => ({[x]: y})))
}

