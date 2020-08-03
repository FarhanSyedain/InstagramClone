/**This file is for the backend and for the frontend purpose of profil page.
 * You can alter some code in this file to customise frontend.
 * Adding loadig animination might make users experince better
 * Load More buttons arnt necessary so they can be removed 
 * note that first code that should be excuted -- besides including other files -- is the code related to Event listners
 * It is better to Add more frontend JS and that will make users day far better
 */

/***The code is very ineffective. It was for the first time i made a massive project.
 * Their are some functions that apparently arnt nessiry but as to make users experice better, i added them
 */



function include(file) {

    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;

    document.getElementsByTagName('head').item(0).appendChild(script);

}

include('../static/js/home.js')




var posts_per_call = 1 // How many Objects we want to get on every fetch call 

//Varibles; Value of whom is equal to objs recived -- Where name suggests obj
var total_posts_recived = 0
var total_tagged_got = 0
var book_marks_recived = 0
var followers_recived = 0
var following_recived = 0


//Fetch calls. Returns Posts of a specific user
function get_posts(time_itr) {

    document.getElementById('load_more_btn').classList.add('hidden') // Hide load more button untill we get posts;check if we have more posts
        //In Db,if so then only display the button

    var max_itr = 3 // How many times should we call this function again, ie. no of recucurtions
    if (time_itr == max_itr) {
        document.getElementById('load_more_btn').classList.remove('hidden') //Diaply -- If we are here that means that we have
            //More Posts,since if we had'nt ,function would have been terminated 
            /**
             * The load more button can be replaced with scrol / i mean if user scrools after the last post -- at a point of time -- /n
             * then call the funtion and load a ton more posts
             */
        return
    }

    var url = '../profile/api/get/data/posts/'
        //Before the fetch , if possible, add a loading animination so that user knows posts are loading
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'user': user, 'total_recived': total_posts_recived, 'posts_per_call': posts_per_call })
        }).then((response) => {
            return response.json()
        })
        .then((data) => {

            var last = data['others']['last']
            var posts = data['posts']

            var has = true
            if (posts == null) {
                //user has no posts
                var has = false
            }

            if (has) {
                total_posts_recived += data['total_recived'] //Change one to No of posts we recive  / // Increment the variable so as to keep record of total posts recived
                    //Hide the animination, if added
                for (i in posts) {

                    var item = ('<div style="max-width:33%;" data-loc="' + posts[i][0] + '"' + 'class="post p-1"><img style="width:100%; height:100%; margin-right:auto; margin-left:auto" src=' + posts[i][1] + '></div>')
                    document.getElementById('postss').innerHTML += item

                }
                if (last) {
                    document.getElementById('load_more_btn').classList.add('hidden')
                        //No more posts now can display the footer -- which we dont have ,lol

                } else {
                    //Recurtion
                    get_posts(time_itr + 1)
                }
            }

        })
}




function get_tagged_posted(time_itrer) {

    document.getElementById('tagged_btn').removeEventListener('click', get_tagged_posted)
    document.getElementById('load_more_tagged').classList.add('hidden')
        //Check weather we have load more button , in case we have add function on click = get_tagged_possted(0) 

    url = '../profile/api/get/data/tagged/posts/'

    var max_iter = 3

    if (time_itrer == max_iter) {
        document.getElementById('load_more_tagged').classList.remove('hidden')
        return
    }

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'total_deleverd': total_tagged_got, 'user': user, 'posts_per_call': posts_per_call })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            var has_tagged = data['is_tagged_in_any']

            if (!has_tagged) { /** we can replace with some logic -- since we don't have posts */ } else {
                total_tagged_got += data['total_recived']

                var tagged = data['tagged']
                var has_more_tagged_posts = data['others']['has_more_tagged_posts']

                for (tagged_post in tagged) {
                    var item = ('<div style="max-width:33%" data-loc="' + tagged[tagged_post][0] + '"' + 'class="post p-1"><img style="width:100%; height:100%; margin-right:auto; margin-left:auto" src=' + tagged[tagged_post][1] + '></div>')
                    document.getElementById('tagged_posts').innerHTML += item
                }
                if (has_more_tagged_posts) {
                    document.getElementById('load_more_tagged').classList.remove('hidden')
                    get_tagged_posted(time_itrer + 1)

                } else {
                    document.getElementById('load_more_tagged').classList.add('hidden')
                    return
                }
            }
        })

}

function load_bookmarks(itr_time) {
    document.getElementById('highlights_btn').removeEventListener('click', load_bookmarks)
    document.getElementById('load_more_bookmarks').classList.add('hidden')

    var max_itr = 3
    if (itr_time == max_itr) {
        document.getElementById('load_more_bookmarks').classList.remove('hidden')
        return
    }

    url = '../profile/api/get/data/bookmarks/posts/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'book_marks_recived': book_marks_recived, 'user': user, 'posts_per_call': posts_per_call })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {

            if (!data['has_book_marks']) {

            } else {

                book_marks_recived += data['total_recived']
                var book_marks = data['book_marks']
                var has_more = data['others']['has_more']

                for (book_mark_obj in book_marks) {

                    var item = ('<div style="max-width:33%" data-loc="' + book_marks[book_mark_obj][0] + '"' + 'class="post p-1"><img style="width:100%; height:100%; margin-right:auto; margin-left:auto" src=' + book_marks[book_mark_obj][1] + '></div>')
                    document.getElementById('book_marks_').innerHTML += item

                }
                if (has_more) {
                    document.getElementById('load_more_bookmarks').classList.add('hidden')
                    load_bookmarks(itr_time + 1)

                } else {
                    document.getElementById('load_more_bookmarks').classList.add('hidden')
                        //Hide Load More Button
                }
            }
        })
}


//Add Two event listners


function get_following(time_itr) {
    document.getElementById('following_btn').removeEventListener('click', get_following)
    url = '../profile/api/get/data/following/users/'

    max_itr = 3

    if (max_itr == time_itr) {
        return //Actually Enable the load more followers button    
    }

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'deliverd': following_recived, 'user': user, 'per_call': 1 })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            if (!data['is_following_anyone']) {} else {
                var following = data['following']
                following_recived += data['others']['deliverd']
                for (obj in following) {
                    if (is_owner == 'True') {
                        //Then Only Unfollow Buttons and if user presses a unfollow button, unfollow the user and remove the div 
                        var username__ = following[obj][2]
                        var name__ = obj
                        var profile_url__ = following[obj][1]
                        var user_id__ = following[obj][0]

                        item = ('<div id="user_following_div' + user_id__ + '"style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + profile_url__ + '" class="img-follower"><a class="follower-name">' + name__ + '</a><br><button  onclick="unfollow_user(' + "'" + username__ + "'" + ')" data-id="' + username__ + '"class="btn btn-info ">Unfollow</button><a href="#" class="follower-link" href="#">' + username__ + '</a> </div>')

                        document.getElementById('following').innerHTML += item

                    } else {
                        //We can have a ton different buttons -- Requested Follow Back Unfollow and Follow.
                        var username__ = following[obj][2]
                        var name__ = obj
                        var profile_url__ = following[obj][1]
                        var user_id__ = following[obj][0]
                        var button_text = following[obj][3][0]
                        var button_on_click = following[obj][3][1]
                        var button_on_click_func_parameters = following[obj][3][2]
                        item = ('<div id="user_following_div' + user_id__ + '"style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + profile_url__ + '" class="img-follower"><a class="follower-name">' + name__ + '</a><br><button id="button_following_id' + username__ + '" onclick="' + button_on_click + "'" + button_on_click_func_parameters + "')" + '" data-id="' + username__ + '"class="btn btn-info ">' + button_text + '</button><a href="#" class="follower-link" href="#">' + username__ + '</a> </div>')

                        document.getElementById('following').innerHTML += item

                    }

                }

                if (data['others']['has_more']) {
                    get_following(time_itr + 1)
                } else {

                    return //No more Followers

                }
            }

        })
}

function get_followers(time_itr) {
    document.getElementById('followers_btn').removeEventListener('click', get_followers)
    url = '../profile/api/get/data/followers/users/'

    max_itr = 3

    if (max_itr == time_itr) {
        return //Actually Enable the load more follwoung button    
    }

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'deliverd': followers_recived, 'user': user, 'per_call': 3 })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            if (!data['is_followed']) {

            } else {

                followers_recived += data['others']['deliverd']
                var followers = data['followers']

                for (obj in followers) {

                    if (is_owner == 'True') {
                        var username__ = followers[obj][2]
                        var name__ = obj
                        var profile_url__ = followers[obj][1]
                        var user_id__ = followers[obj][0]

                        item = ('<div id="follower_user_id' + user_id__ + '"  style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + profile_url__ + '" class="img-follower"><a class="follower-name">' + name__ + '</a><br> <i onclick="remove_follower(' + "'" + username__ + "'" + ')" class="fa fa-close"></i>  <a href="#" class="follower-link" href="#">' + username__ + '</a></div>')

                        document.getElementById('followers').innerHTML += item

                    } else {
                        var username__ = followers[obj][2]
                        var name__ = obj
                        var profile_url__ = followers[obj][1]
                        var user_id__ = followers[obj][0]
                        var button_text = followers[obj][3][0]
                        var button_on_click = followers[obj][3][1]
                        var button_on_click_func_parameters = followers[obj][3][2]

                        item = ('<div id="user_following_div' + user_id__ + '"style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + profile_url__ + '" class="img-follower"><a class="follower-name">' + name__ + '</a><br><button id="_button_following_id' + username__ + '" onclick="' + button_on_click + "'" + button_on_click_func_parameters + "')" + '" data-id="' + username__ + '"class="btn btn-info ">' + button_text + '</button><a href="#" class="follower-link" href="#">' + username__ + '</a> </div>')

                        document.getElementById('followers').innerHTML += item

                    }
                }

                if (data['others']['has_more']) {
                    get_followers(time_itr + 1)
                } else {
                    return //No more Followers
                }
            }

        })


}


function unfollow_user(username) {

    /**Unfollows a user and then removes the div. Note for owner only */

    url = '../profile/api/get/data/remove/following/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'username': username, 'user_': user })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if (data['success']) {
                try {
                    var id = 'user_following_div' + data['id']
                    document.getElementById(id).outerHTML = ''
                } catch (err) {

                }
                reset_following_count()
            } else {

            }
        })


}


function remove_follower(username) {
    /**Removes a follower and then removes the div */
    url = '../profile/api/get/data/remove/follower/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'user': user, 'username': username })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if (data['success']) {
                document.getElementById('follower_user_id' + data['id']).outerHTML = ''
                reset_folllowers_count()
            } else {

            }
        })


}

function reset_following_count() {

    url = '../profile/api/get/data/get/following/count'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'user': user })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            var count_ = data['count']
            document.getElementById('__following__count').innerHTML = count_
        })

}

function reset_folllowers_count() {
    url = '../profile/api/get/data/get/followers/count'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'user': user })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            var count_ = data['count']
            document.getElementById('__following_count_____').innerHTML = count_
        })
}



function _follow_user(username) {
    /** Follows a user and programmed for profile page only*/


    url = '../genral/api/follow/user'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'username': username, })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            if (data['success']) {
                document.getElementById('button_following_id' + username).removeAttribute('onclick')
                if (data['Requested']) {
                    try {
                        document.getElementById('button_following_id' + username).innerHTML = 'Requested'
                        document.getElementById('button_following_id' + username).setAttribute('onclick', '_del_req(' + "'" + username + "'" + ')')
                    } catch (err) {

                    }
                    try {
                        document.getElementById('_button_following_id' + username).innerHTML = 'Requested'
                        document.getElementById('_button_following_id' + username).setAttribute('onclick', '_del_req(' + "'" + username + "'" + ')')
                    } catch (err) {

                    }
                } else {
                    try {
                        document.getElementById('button_following_id' + username).innerHTML = 'Unfollow '
                        document.getElementById('button_following_id' + username).setAttribute('onclick', '_unfollow_user(' + "'" + username + "'" + ')')
                    } catch (err) {

                    }
                    try {
                        document.getElementById('_button_following_id' + username).innerHTML = 'Unfollow '
                        document.getElementById('_button_following_id' + username).setAttribute('onclick', '_unfollow_user(' + "'" + username + "'" + ')')
                    } catch (err) {

                    }

                }
            }
        })


}

function _unfollow_user(username) {
    url = '../genral/api/unfollow/user'
    console.log(username)
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'username': username })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            if (data['success']) {
                try {
                    document.getElementById('button_following_id' + username).removeAttribute('onclick')
                    if (data['Follows']) {
                        document.getElementById('button_following_id' + username).innerHTML = 'Follow Back'
                    } else {
                        document.getElementById('button_following_id' + username).innerHTML = 'Follow '
                    }
                    document.getElementById('button_following_id' + username).setAttribute('onclick', '_follow_user(' + "'" + username + "'" + ')')
                } catch (err) {

                }
                console.log('I am here at least')
                try {
                    document.getElementById('_button_following_id' + username).removeAttribute('onclick')
                    if (data['Follows']) {
                        document.getElementById('_button_following_id' + username).innerHTML = 'Follow Back'
                    } else {
                        document.getElementById('_button_following_id' + username).innerHTML = 'Follow '
                    }
                    console.log('I m djkaljs')
                    document.getElementById('_button_following_id' + username).setAttribute('onclick', '_follow_user(' + "'" + username + "'" + ')')
                } catch (err) {
                    console.log(err, 'Hellow')
                }

            }
        })


}

function _del_req(username) {

    url = '../genral/api/delete/follow-request'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'username': username })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            if (data['success']) {

                if (data['Follows']) {
                    try {
                        document.getElementById('button_following_id' + username).innerHTML = 'Follow Back'
                    } catch (err) {

                    }
                    try {
                        document.getElementById('_button_following_id' + username).innerHTML = 'Follow Back'
                    } catch (err) {

                    }
                } else {
                    try {
                        document.getElementById('button_following_id' + username).innerHTML = 'Follow'
                    } catch (err) {

                    }
                    try {
                        document.getElementById('_button_following_id' + username).innerHTML = 'Follow'
                    } catch (err) {

                    }
                }
                try {
                    document.getElementById('button_following_id' + username).removeAttribute('onclick')
                    document.getElementById('button_following_id' + username).setAttribute('onclick', '_follow_user(' + "'" + username + "'" + ')')
                } catch (err) {

                }
                try {
                    document.getElementById('_button_following_id' + username).removeAttribute('onclick')
                    document.getElementById('_button_following_id' + username).setAttribute('onclick', '_follow_user(' + "'" + username + "'" + ')')
                } catch (err) {

                }
            }
        })

}

function get_yourself() {
    url = '../profile/api/get/data/get_yourself'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({})
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            user_id__ = data['id']
            profile_url__ = data['profile_url__']
            name__ = data['name']
            username__ = data['username']
            item = ('<div id="user_following_div' + user_id__ + '"style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + profile_url__ + '" class="img-follower"><a class="follower-name">' + name__ + '</a><br><a href="#" class="follower-link" href="#">' + username__ + '</a> </div>')

            document.getElementById('followers').innerHTML += item
        })
}

function __del_req(username) {
    url = '../genral/api/delete/follow-request'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'username': username })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            if (data['success']) {

                if (data['Follows']) {
                    document.getElementById('Head_button_action').innerHTML = 'Follow Back'
                    document.getElementById('Head_button_action').removeAttribute('onclick')
                    document.getElementById('Head_button_action').setAttribute('onclick', '__follow_user(' + "'" + username + "'" + "')")
                } else {
                    document.getElementById('Head_button_action').innerHTML = 'Follow '
                    document.getElementById('Head_button_action').removeAttribute('onclick')
                    document.getElementById('Head_button_action').setAttribute('onclick', '__follow_user(' + "'" + username + "'" + "')")
                }
            }
        })
}

function __follow_user(username) {
    url = '../genral/api/follow/user'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'username': username, })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            if (data['success']) {

                if (data['Requested']) {
                    document.getElementById('Head_button_action').innerHTML = 'Requested'
                    document.getElementById('Head_button_action').removeAttribute('onclick')
                    document.getElementById('Head_button_action').setAttribute('onclick', '__del_req(' + "'" + username + "'" + ")")
                } else {
                    document.getElementById('Head_button_action').innerHTML = 'Unfollow'
                    document.getElementById('Head_button_action').removeAttribute('onclick')
                    document.getElementById('Head_button_action').setAttribute('onclick', '__unfollow_user(' + "'" + username + "'" + ")")
                    get_yourself()
                }
            }
        })
}

function __unfollow_user(username) {
    url = '../profile/api/get/data/remove/following/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'username': username, 'user_': req_user })
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if (data['success']) {
                try {
                    var id = 'user_following_div' + data['id_t']
                    console.log(id, data['success'])
                    document.getElementById(id).outerHTML = ''
                    document.getElementById('Head_button_action').innerHTML = 'Follow'
                    document.getElementById('Head_button_action').removeAttribute('onclick')
                    document.getElementById('Head_button_action').setAttribute('onclick', '__follow_user' + "('" + username + "')")

                } catch (err) {
                    console.log(err)
                }
                reset_following_count()
            } else {

            }
        })
}

if (is_owner == 'True' || show == 'True') {

    //instead of added event listerns it is calling the function.. Try to sove the next four lines

    document.getElementById('tagged_btn').addEventListener('click', get_tagged_posted(0))
    document.getElementById('highlights_btn').addEventListener('click', load_bookmarks(0))
    document.getElementById('following_btn').addEventListener('click', get_following(0))
    document.getElementById('followers_btn').addEventListener('click', get_followers(0))
    get_posts(0)


}
//For Load More Buttons
function load_more_tagged_posts() { get_tagged_posted(0) }

function load_more_posts() { get_posts(0) }