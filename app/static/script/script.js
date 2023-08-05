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
        const form = formSerialize("#admin-loginform")
        const request = await  $.ajax({
            method: `POST`,
            url: `/super/login_process`,
            data: {...form, role:role},
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
        const form = formSerialize("#signupform")

     const request = await   $.ajax({
            method: `POST`,
            url: `/signup`,
            data: form,
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
                $('#signupform').trigger("reset");
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
        console.log(request)
        if (!request.status){

            toastr.error(request.message)

        }else {
            toastr.success(request.message)
            for (const value of request.data) {
                setTimeout(() => {

                    window.location.href = `/search?adult=${data.adult}&children=${data.children}&response=${JSON.stringify({route:value.routeId,bus:value.busId,ticket:value.id})}&status=true`
                }, 1000)
            }
        }
    }
    catch (error){
        toastr.error(error)
    }
})


if (window.location.pathname === `/admin/bus/add`) {
    try {



        $(`#add-bus-btn`).click(async function(e) {
            const form = formSerialize("#addbus")
            const request = await $.ajax({
                method: `POST`,
                url: `/admin/bus/add_process`,
                data: form,
                dataType: `json`,
                beforeSend: function () {
                    $(`#add-bus-btn`).addClass(`d-none`)
                    $(`#add-bus-spinner`).removeClass(`d-none`)
                },
                complete: function () {
                    $(`#add-bus-btn`).removeClass(`d-none`)
                    $(`#add-bus-spinner`).addClass(`d-none`)
                }
            })

            if (request.status) {
                toastr.success(request.message)
                $('#addbus').trigger("reset");
            } else {
                toastr.error(request.message)
            }
        })
    }catch (error) {
        toastr.error(error)
    }

}
if (window.location.pathname === `/admin/routes/add`) {
    try {

        $(`#add-route-btn`).click(async function(e) {
            const form = formSerialize("#addroute")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/admin/route/add_process`,
                data: form,
                dataType: `json`,
                beforeSend: function () {
                    $(`#add-route-btn`).addClass(`d-none`)
                    $(`#add-route-spinner`).removeClass(`d-none`)
                },
                complete: function () {
                    $(`#add-route-btn`).removeClass(`d-none`)
                    $(`#add-route-spinner`).addClass(`d-none`)
                }
            })

            if (request.status) {
                toastr.success(request.message)
                $('#addroute').trigger("reset");
            } else {
                toastr.error(request.message)
            }
        })
    }catch (error) {
        toastr.error(error)
    }

}
if (window.location.pathname === `/admin/ticket/add`) {
    try {

        $(`#add-ticket-btn`).click(async function(e) {
            const form = formSerialize("#addticket")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/admin/ticket/add_process`,
                data: form,
                dataType: `json`,
                beforeSend: function () {
                    $(`#add-ticket-btn`).addClass(`d-none`)
                    $(`#add-ticket-spinner`).removeClass(`d-none`)
                },
                complete: function () {
                    $(`#add-ticket-btn`).removeClass(`d-none`)
                    $(`#add-ticket-spinner`).addClass(`d-none`)
                }
            })

            if (request.status) {
                toastr.success(request.message)
                $('#addticket').trigger("reset");
            } else {
                toastr.error(request.message)
            }
        })
    }catch (error) {
        toastr.error(error)
    }

}
