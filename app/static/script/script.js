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
                label: req.data[x].name,
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
                    window.location.reload(true)
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
        console.log(form)
        const request = await  $.ajax({
            method: `POST`,
            url: `/control/login_process`,
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
        console.log(request)



            if (request.status) {
                login_modal.modal('hide');
                setTimeout(() => {
                    window.location.href = `/control/overview`
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

//user profile

$(`.delete_user`).click(async function(e) {

    try {



        if (confirm(`Do you want to delete user? This action cannot be reversed.`)) {
            const request = await $.ajax({
                method: `GET`,
                url: `/control/user/delete`,
                data: {id: e.target.dataset.id},
                dataType: `json`,
                beforeSend: function () {
                    e.target.disabled = true
                },
                complete: function () {
                    e.target.disabled = false
                }
            })


            if (request.status) {
                toastr.success(request.message)
                setTimeout(() => {
                    window.location.reload()
                }, 800)
            } else {
                toastr.error(request.message)
            }
        }
    }catch (error) {
        toastr.error(error)
    }

})

$(`.user_profile_update`).click(async function(e) {

    try {
        const form = formSerialize(".userprofileform")
        console.log(form)
        const request = await   $.ajax({
            method: `POST`,
            url: `/profile/update`,
            data: form,
            dataType: `json`,
            beforeSend: function (){
             e.target.disabled = true
            },
            complete: function () {
              e.target.disabled = false
            }
        })


        if (request.status) {
            toastr.success(request.message)
            setTimeout(()=>{
               window.location.reload()
            }, 800)
        }
        else {
            toastr.error(request.message)
        }
    }catch (error) {
        toastr.error(error)
    }

})
$(`.user_profile_password_update`).click(async function(e) {

    try {
        const form = formSerialize(".userprofilepasswordform")

        const request = await   $.ajax({
            method: `POST`,
            url: `/profile/password/update`,
            data: form,
            dataType: `json`,
            beforeSend: function (){
             e.target.disabled = true
            },
            complete: function () {
              e.target.disabled = false
            }
        })


        if (request.status) {
            toastr.success(request.message)
            $('.userprofilepasswordform').trigger("reset");
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
            setTimeout(() => {

                    window.location.href = `/search?departure=${data.departure_date}&adult=${data.adult}&children=${data.children}&response=${JSON.stringify(request.data)}&status=true`
                }, 1000)

        }
    }
    catch (error){
        toastr.error(error)
    }
})


if (window.location.pathname === `/control/bus/add`) {
    try {



        $(`#add-bus-btn`).click(async function(e) {
            const form = formSerialize("#addbus")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/control/bus/add_process`,
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
if (window.location.pathname === `/control/bus/stop/add`) {
    try {



        $(`#add-bus-btn`).click(async function(e) {
            const form = formSerialize("#addbus_stop")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/control/bus/stop/add_process`,
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
                $('#addbus_stop').trigger("reset");
            } else {
                toastr.error(request.message)
            }
        })
    }catch (error) {
        toastr.error(error)
    }

}
if (window.location.pathname === `/control/reservations/search` || window.location.pathname === `/control/overview`) {
    try {



        $(`#reserve-search-btn`).click(async function(e) {
            const form = formSerialize("#reservesearchform")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/control/reservations/search_process`,
                data: form,
                dataType: `json`,
                beforeSend: function () {
                    $(`#reserve-search-btn`).addClass(`d-none`)
                    $(`#reserve-search-spinner`).removeClass(`d-none`)
                },
                complete: function () {
                    $(`#reserve-search-btn`).removeClass(`d-none`)
                    $(`#reserve-search-spinner`).addClass(`d-none`)
                }
            })

            if (request.status) {
                toastr.success(request.message)
                setTimeout(()=> {
                    window.location.href = `/control/reservations/search/result?number=${request.data.reservation_number}&status=true`
                },1000)
            } else {
                toastr.error(request.message)
            }
        })
    }catch (error) {
        toastr.error(error)
    }

}
if (window.location.pathname === `/control/routes/add`) {
    try {

        $(`#add-route-btn`).click(async function(e) {
            const form = formSerialize("#addroute")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/control/route/add_process`,
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
if (window.location.pathname === `/control/ticket/add`) {
    try {

        $(`#add-ticket-btn`).click(async function(e) {
            const form = formSerialize("#addticket")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/control/ticket/add_process`,
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
if (window.location.pathname === `/control/ticket/edit`) {
    try {

        $(`#edit-ticket-btn`).click(async function(e) {
            const form = formSerialize("#editticket")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/control/ticket/edit_process`,
                data: form,
                dataType: `json`,
                beforeSend: function () {
                    $(`#edit-ticket-btn`).addClass(`d-none`)
                    $(`#edit-ticket-spinner`).removeClass(`d-none`)
                },
                complete: function () {
                    $(`#edit-ticket-btn`).removeClass(`d-none`)
                    $(`#edit-ticket-spinner`).addClass(`d-none`)
                }
            })

            if (request.status) {
                toastr.success(request.message)
                window.location.reload()
            } else {
                toastr.error(request.message)
            }
        })
    }catch (error) {
        toastr.error(error)
    }

}
if (window.location.pathname === `/control/routes/edit`) {
    try {

        $(`#edit-route-btn`).click(async function(e) {
            const form = formSerialize("#editroute")
            console.log(form)
            const request = await $.ajax({
                method: `POST`,
                url: `/control/routes/edit_process`,
                data: form,
                dataType: `json`,
                beforeSend: function () {
                    $(`#edit-route-btn`).addClass(`d-none`)
                    $(`#edit-route-spinner`).removeClass(`d-none`)
                },
                complete: function () {
                    $(`#edit-route-btn`).removeClass(`d-none`)
                    $(`#edit-route-spinner`).addClass(`d-none`)
                }
            })

            if (request.status) {
                toastr.success(request.message)
                window.location.reload()
            } else {
                toastr.error(request.message)
            }
        })
    }catch (error) {
        toastr.error(error)
    }

}

$(`.cancel_reservation`).click(async function(e){
    e.preventDefault()
    try {
        const id = e.target.dataset.id
        const request = await $.ajax({
            method: `GET`,
            url: `/reservation/cancel`,
            data: {uid:id },
            dataType: `json`,
            beforeSend: function () {
               e.target.disabled = true
            },
            complete: function (){
                e.target.disabled = false
            }
        })
        console.log(request)
        if (!request.status){

            toastr.error(request.message)
            setTimeout(()=>{window.location.reload()}, 800)

        }else {
            toastr.success(request.message)
        }
    }
    catch (error){
        toastr.error(error)
    }


})

