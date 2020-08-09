var last_ = 0
function get_requests(){

    //Loads friend requests
    url = '../friend_reqs/data/get'

    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'last':last_ , 'per_call':1 })
    }).then((resp)=>{
        return resp.json()
    }).then((data)=>{

        if (! data['proceed']){
            document.getElementById('mai____').innerHTML += ('<p>No friend requests</p>')
        
        }
        else{
            last_  += data['recived']
            for ( obj of data['requests'] ){

                img_url = obj[0]
                username = obj[1]
                item = ('<div id="fdsfdsaf'+ username+'" style="width: 300px;" class="col-sm bg-white text-center p-2"><img style="width: 50px;height:50px;border-radius:100%" src="..'+ img_url +'"><a href="../'+username+'">@'+username +'</a><div class="mb-1"></div><button id="fdasfdsafewb'+ username +'" onclick="accept_('+ "'"  + username  +  "'" +')" class="btn btn-sm btn-success">Accept</button><button  id="fdasfdsfdsfdsafewb'+ username +'"  onclick="reject_('+ "'"  + username  +  "'" +')" class="btn btn-sm btn-danger">Reject</button></div>')
                
                document.getElementById('mai____').innerHTML += item
            }
            if (data['has_more']){
            
         
            }
            else{

            }
        }

    })


}


function reject_(username){

    url = '../friend_reqs/reject'
    document.getElementById('fdasfdsafewb'+username).setAttribute('disabled','disabled')
    fetch(url,{
        
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'username':username})
    })
        .then((resp)=>{
            return resp.json()
        })
        .then((data)=>{
            last_ -=1

            get_requests()

            document.getElementById('fdsfdsaf'+username).outerHTML = ''
        })
}



function accept_(username){

    url = '../friend_reqs/accept'
    document.getElementById('fdasfdsfdsfdsafewb'+username).setAttribute('disabled','disabled')
    fetch(url,{
        
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'username':username})
    })

        .then((resp)=>{
            return resp.json()
        })
        .then((data)=>{
            last_ -=1
            document.getElementById('fdsfdsaf'+username).outerHTML = ''
            get_requests()

        })



}



get_requests()