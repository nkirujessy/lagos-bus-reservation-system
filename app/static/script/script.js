const login_modal = $(`#loginPopupForm`)
const register_modal = $(`#signupPopupForm`)



const fetchlocations = async ()=> {
    const req = await $.ajax({
        url: `/locations`,
        method: `GET`,
        dataType: `JSON`
    });


    if (req.status){
        const locations = []
        const ids = []
        //
        for (const x in req.data){

            locations.push({
                label: req.data[x].location,
                value: req.data[x].id
            })
        }

        $( "#start_route" ).autocomplete({
            source: locations,
            focus: function (event, ui) {
                $( "#start_route" ).val( ui.item.label );
                return false
            },
            select: function( event, ui ) {
                console.log(event, ui)
                $( "#start_route" ).val( ui.item.label );
                $( "#start_route_id" ).val( ui.item.value );
                return false
            }
        })
        $( " #end_route" ).autocomplete({
            source: locations,
            focus: function (event, ui) {
                $( "#end_route" ).val( ui.item.label );
                return false
            },
            select: function( event, ui ) {
                console.log(event, ui)
                $( "#end_route" ).val( ui.item.label );
                $( "#end_route_id" ).val( ui.item.value );
                return false
            }
        })

    }
}


console.log(window.location.pathname)
if (pathname === ``) {
    fetchlocations()
}
//login
$(`#login`).click( async function() {
    try {
        const data = {
            email: $(`#loginemail`).val(),
            password: $(`#loginpassword`).val()
        }
        const request = await  $.ajax({
            method: `POST`,
            url: `/login`,
            data: data,
            dataType: `json`,
            beforeSend: function (){
                $(`#login`).addClass(`d-none`)
                $(`#spinner-btn-login`).removeClass(`d-none`)
            },
            complete: function (){
                $(`#login`).removeClass(`d-none`)
                $(`#spinner-btn-login`).addClass(`d-none`)
            }
        })

            if (request.status) {
                login_modal.modal('hide');
                setTimeout(() => {
                    window.location.href = `/app/overview`
                }, 800)
                toastr.success(request.message)
            } else {
            toastr.error(request.message)
            }
    }catch (error){
        toastr.error(error)
    }

})
$(`#admin-login`).click( async function() {
    try {
        const role = (window.location.pathname === `/admin/login`)?`admin`: `driver`
        const data = {
            email: $(`#super-email`).val(),
            password: $(`#super-password`).val(),
            role: role
        }
        const request = await  $.ajax({
            method: `POST`,
            url: `/super/login_process`,
            data: data,
            dataType: `json`,
            beforeSend: function (){
                $(`#admin-login`).addClass(`d-none`)
                $(`.spinner-btn-login`).removeClass(`d-none`)
            },
            complete: function (){
                $(`#admin-login`).removeClass(`d-none`)
                $(`.spinner-btn-login`).addClass(`d-none`)
            }
        })

            if (request.status) {
                login_modal.modal('hide');
                setTimeout(() => {
                    window.location.href = `/admin/overview`
                }, 800)
                toastr.success(request.message)
            } else {
            toastr.error(request.message)
            }
    }catch (error){
        toastr.error(error)
    }

})

//signup
$(`#signup`).click(async function() {

    try {
        const data = {
            email: $(`#signupemail`).val(),
            password: $(`#signuppass`).val(),
            name: $(`#signupfname`).val(),
            confirmpassword: $(`#signupconfirmpass`).val()
        }

     const request = await   $.ajax({
            method: `POST`,
            url: `/signup`,
            data: data,
            dataType: `json`,
            beforeSend: function (){
                $(`#signup`).addClass(`d-none`)
                $(`#spinner-btn`).removeClass(`d-none`)
            },
         complete: function () {
             $(`#signup`).removeClass(`d-none`)
             $(`#spinner-btn`).addClass(`d-none`)
         }
        })


            if (request.status) {
                toastr.success(request.message)
                register_modal.modal('hide');
                setTimeout(()=> {
                    login_modal.modal('show');
                }, 1000)
            }
            else {
                toastr.error(request.message)
            }
    }catch (error) {
        toastr.error(error)
    }

})


$(`#search-bus`).click(async function(e){
    e.preventDefault()
    try {

        const adult = $(`#adult_pass`).html().match(/\d/g)[0]
        const children = $(`#children_pass`).html().match(/\d/g)[0]
        const data = {
            start_route: $(`#start_route_id`).val(),
            end_route: $(`#end_route_id`).val(),
            departure_date: $(`#dept_date`).val(),
                 adult: adult,
            children: children

        }

        console.log(data)
        const request = await $.ajax({
            method: `POST`,
            url: `/api/bussearch`,
            data: data,
            dataType: `json`,
            beforeSend: function () {
                $(`#search-bus`).addClass(`d-none`)
                $(`#spinner-btn-search`).removeClass(`d-none`)
            },
            complete: function (){
                $(`#search-bus`).removeClass(`d-none`)
                $(`#spinner-btn-search`).addClass(`d-none`)
            }
        })

        if (!request.status){
            setTimeout(() => {
                window.location.href = `/search?result=false`
            }, 500)

        }else {
            setTimeout(() => {
                window.location.href = `/search?start=${data.start_route}&end=${data.end_route}&departure=${data.departure_date}&adult=${data.adult}&children=${data.children}&ticket=`
            }, 500)
        }
    }
    catch (error){
        toastr.error(error)
    }
})

