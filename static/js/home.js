//JS for home page

var total_posts_recived = 0
var total_stories_recived = 0
var total_comments_recived = 0



function like_unlike_post(id) {

    var like_btn = document.getElementById('like' + id)
    if (like_btn.classList.contains('non-like')) {
        //Then like the post
        like_btn.classList.remove('non-like')
        like_btn.classList.add('like')

        url = '../genral/api/like_post'

        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'id': id })
            })
            .then((resp) => {
                return resp.json()
            }).then((data) => {
                var count = data['count']
                document.getElementById('like_count__' + id).innerHTML = count

            })

    } else {
        //Then dislike the post
        like_btn.classList.remove('like')
        like_btn.classList.add('non-like')

        url = '../genral/api/unlike_post'

        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'id': id })
            })
            .then((resp) => {
                return resp.json()
            })
            .then((data) => {
                var count = data['count']
                document.getElementById('like_count__' + id).innerHTML = count

            })
    }
}

function add_remove_bookmark(id) {

    var bookmark_btn = document.getElementById('bookmark' + id)

    if (bookmark_btn.classList.contains('non-marked')) {

        //Then bookmark the post

        bookmark_btn.classList.remove('non-marked')
        bookmark_btn.classList.add('marked')

        url = '../genral/api/add_bookmark'

        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'id': id })
            })
            .then((resp) => {
                return resp.json()
            })
    } else {

        //Then unmark the post

        bookmark_btn.classList.add('non-marked')
        bookmark_btn.classList.remove('marked')

        url = '../genral/api/remove_bookmark'

        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'id': id })
            })
            .then((resp) => {
                return resp.json()
            })
    }
}


function prepare_comment(scope_, user_name,comment_id) {

    if (scope_ == 'global') {
        //Then we are supposed to add the commnent to all coments
        document.getElementById('ReplyBox').value = ' '
        document.getElementById('ReplyBox').focus()
        document.getElementById('ReplyBox').setAttribute('data-scope', 'global')
        document.getElementById('ReplyBox').setAttribute('data-user_name', 'null')

    } else {
        //Then add coment to replies of a comment
        document.getElementById('ReplyBox').setAttribute('data-scope', 'local')
        document.getElementById('ReplyBox').setAttribute('data-user_name', user_name)
        document.getElementById('ReplyBox').setAttribute('data-comment_id', comment_id)
        document.getElementById('ReplyBox').value = '@' + user_name + ' '
        document.getElementById('ReplyBox').focus()
    }

}

function post_comment() {
    var comment_body = document.getElementById('ReplyBox').value.trim()
    var comment_scope = document.getElementById('ReplyBox').dataset.scope
    var comment_user = document.getElementById('ReplyBox').dataset.user_name

    if (comment_body.length == 0) {
        return
    }
    document.getElementById('ReplyBox').value = ''
    if (comment_scope == 'global') {
        url = '../genral/api/add_comment_globally'

        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'comment_body': comment_body, 'post_id': post_id })
            })
            .then((resp) => {
                return resp.json()
            })
            .then((data) => {

                if (data['success']) {
                    //Then load that comment
                    var total_comments = data['total_comments']
                    document.getElementById('comment_____count___').innerHTML = total_comments
                    load_comments()
                }
            })
    } else {
        var reply_to = document.getElementById('ReplyBox').dataset.comment_id

     

        url = '../post/api/reply_to_comment'

        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'id':reply_to, 'comment_body':comment_body })
            })
        .then((resp)=>{
            return resp.json()
        })
        .then((data)=>{
            if (! data['error']){
            
                    document.getElementById('____________fdsfds_______'+reply_to).innerHTML = data['reply_count']
                    try{
                        get_and_render_replies(reply_to,data['reply_count']-1)}
                    catch(err){
                        
                    }
                    try{
                        document.getElementById('____________fdsfds_____________'+reply_to).classList.remove('hidden')
                    }catch(err){

                    }
    
            }else{
                //The comment has been deleted
            }
        })


    }
}


function post_comment_(id) {

    var comment_body = document.getElementById('commentdata' + id).value.trim()

    document.getElementById('commentdata' + id).value = ''
    if (comment_body.length == 0) {
    } else {
    

        document.getElementById('post_adder' + id).setAttribute('disabled', 'disabled')

        url = '../genral/api/add_comment_globally'

        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'comment_body': comment_body, 'post_id': id })
            })
            .then((resp) => {
                return resp.json()
            })
            .then((data) => {
                document.getElementById('post_adder' + id).removeAttribute('disabled')
                total_comments_ = data['total_comments']
                document.getElementById('comment___count' + id).innerHTML = total_comments_
                load_comments()

            })
    }

}

function open_comment_sec(id) {

    var comment_btn = document.getElementById('comment' + id)

    if (comment_btn.classList.contains('hidden')) {
        comment_btn.classList.remove('hidden')
    } else {
        comment_btn.classList.add('hidden')

    }

}
if (page == 'home'){




function load_posts() {

    url = '../home/api/get/data/posts'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'per_call': 2, 'recived': total_posts_recived })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {

            if (!data['proceed']) {

                document.getElementById('Loading_ASFSDFS_DSFASDFSDA').outerHTML = ''

                //There fore we dont have any posts to display
            } else {
                total_posts_recived = total_posts_recived + data['others']['deleverd']
                posts = data['posts']
                for (post in posts) {

                    var class_for_bookmark
                    var class_for_like_button

                    if (posts[post][2]) {
                        class_for_bookmark = 'marked'
                    } else {
                        class_for_bookmark = 'non-marked'
                    }

                    if (posts[post][4]) {
                        class_for_like_button = 'like'
                    } else {
                        class_for_like_button = 'non-like'
                    }

                    total_likes = posts[post][0]
                    post_url = posts[post][3]
                    total_comments = posts[post][1]
                    post_caption = posts[post][6]
                    post_author = posts[post][5]
                    post_dated = posts[post][7]
                    item = (' <div  style="margin: auto;" class="col-sm p-1 bg-light"><span class="mb-2">' + post_author + '| ' + post_dated + '</span><br><img src="..' + post_url + ' " class="post-img" alt=""><span> <span id="like_count__' + post + '"> ' + total_likes + '</span> Likes <i onclick="like_unlike_post(' + "'" + post + "'" + ')" id="like' + post + '"  style="font-size: 1.5em;"  class="fa ' + class_for_like_button + ' fa-heart like_buttons"></i> <i onclick="open_comment_sec(' + post + ')" id="comment-btn' + post + '"   style="font-size: 1.5em;" class="fa fa-comments comment_button"></i> <i onclick="add_remove_bookmark(' + post + ')" id="bookmark' + post + '"  style="font-size:1.5em ;" class="fa fa-bookmark book_marks ' + class_for_bookmark + '  "></i> <a href="#">View All <span id="comment___count' + post + '"> ' + total_comments + ' </span> Comments</a></span><div id="comment' + post + '" class="hidden" ><textarea id="commentdata' + post + '" class="form-control" placeholder="..." rows="2"></textarea><button id="post_adder' + post + '" onclick="post_comment_(' + post + ')" id="addcomment' + post + '" style="margin: auto;display:block" class="btn btn-outline-success mt-1 mb-2 add_comments">Post</button></div><p>' + post_caption + '</p></div> ')
                    document.getElementById('______all_posts____').innerHTML += item
                }
                if (data['others']['has_more']) {
                    load_posts()
                } else {
                    document.getElementById('Loading_ASFSDFS_DSFASDFSDA').outerHTML = ''
                }
            }

        })
}}


if (page == 'detail'){
try{
function delete__post(){
    
    document.getElementById('____________________FDSFSDfsdf__').setAttribute('disabled','disabled')

    url = '../post/api/delete_post'

    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'id':post_id })

    })
    .then((resp)=>{
        return resp.json()
    })
    .then((data)=>{
        if (data['success']){
            window.location = '../'

        }else{
            //POSt isnt deleted due to some weird causes
        }
    })

}}catch(err){
    
}
function load_comments(){

    url = '../post/api/get/data/comments'

    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'id':post_id , 'per_call': 5, 'deliverd': total_comments_recived })
    })
    .then((resp)=>{
        return resp.json()
    })
    .then((data)=>{
        if (!data['proceed']){
            //we dont have any comments
        }else{  
        total_comments_recived += data['recived']


        for (comment of data['comments'] ){
            comment_body = comment[0]
            comment_author = comment[1]
            comment_author_image = comment[2]
            comment_posted = comment[3]
            comment_id =  comment[5]
            reply_count = comment[4]
           
            if (reply_count != 0){
                item = ('<div><div class="bg-light p-1 mb-2"><img src="..'+comment_author_image+'" class="image-com"><span><a href="#">@'+ comment_author +'  </a> <p style="white-space: pre-wrap;word-break:break-all">'+ comment_body +'</p> </span><span>' +comment_posted+  ' | <a onclick="prepare_comment('+ "'" + 'local' + "'"  + "," + "'" + comment_author + "'," + comment_id   +')"   class="text-info rep">Reply</a> |  <a onclick="show___replies__('+ comment_id +')"  id="____________fdsfds_____________'+comment_id +'"> View All  <span id="____________fdsfds_______'+ comment_id  +'" > ' + reply_count + '</span> Replies </a> </a> </span></div> <div id="_____SDVA_VSES_replies'+ comment_id+'" class="ml-4 container hidden p-2"></div>  </div>')
            }else{
                item = ('<div><div class="bg-light p-1 mb-2"><img src="..'+comment_author_image+'" class="image-com"><span><a href="#">@'+ comment_author +'  </a> <p style="white-space: pre-wrap;word-break:break-all">'+ comment_body +'</p> </span><span>' +comment_posted+  ' | <a onclick="prepare_comment('+ "'" + 'local' + "'"  + "," + "'" + comment_author + "',"  + comment_id  +')"   class="text-info rep">Reply</a> <span  onclick="show___replies__('+ comment_id +')"  class="hidden" id="____________fdsfds_____________'+ comment_id +'">View All <span id="____________fdsfds_______'+ comment_id  +'" > ' + reply_count + '</span> Replies </span>   </span></div> <div id="_____SDVA_VSES_replies'+ comment_id+'" class="ml-4 container p-2 hidden"> </div> </div>')
            }
            document.getElementById('allllll___________comments').innerHTML += item
        }

            
        if (data['has_more']){
            //We have more comments
            load_comments()
        }
        else{
            //No more comments
        }
        }

    })



}

function show___replies__(id){
    
    id_ = '_____SDVA_VSES_replies'+id
    document.getElementById(id_).classList.remove('hidden')
    document.getElementById('____________fdsfds_____________'+id).removeAttribute('onclick')

    get_and_render_replies(id,0)



}

function get_and_render_replies(id,rec){

    url = '../post/api/get/data/comment/replies'

    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'id':id , 'per_call':2, 'deliverd':rec})
    })
    .then((resp)=>{
        return resp.json()
    })
    .then((data)=>{
        rec += data['recived']
        comment_replies = data['replies']

        for (reply of comment_replies){

            username__  = reply[1]
            urlimage__  = reply[2]
            content__   = reply[0]
            dated__  = reply[3]


            item = ('<div class="bg-light border-4 border-warning border-top-success p-1 mb-2"><img src="..'+urlimage__+'" class="image-com"><span><a href="#">@'+ username__ +'  </a>  <p style="white-space: pre-wrap;word-break:break-all">'+ content__ +'</p> </span> <p>'+ dated__ +'</p></div>')

            document.getElementById('_____SDVA_VSES_replies'+id).innerHTML += item

        }

        if (data['has_more']){
            get_and_render_replies(id,rec)
        }else{
            
        }
    })
    
}}




if (page == 'home'){
    
    load_posts()

    
}else{
    
    load_comments()
}
