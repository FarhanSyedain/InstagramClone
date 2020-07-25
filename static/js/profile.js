function include(file) {

    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;

    document.getElementsByTagName('head').item(0).appendChild(script);

}

include('../static/js/backend.js')
include('../static/js/home.js')


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var csrftoken = getCookie('csrftoken');
var total_posts_recived = 0
var posts_per_call = 1
var total_tagged_got = 0
var book_marks_recived = 0
var followers_recived = 0
var following_recived = 0

function get_posts(time_itr) {

    document.getElementById('load_more_btn').classList.add('hidden')

    if (time_itr == 3) {
        document.getElementById('load_more_btn').classList.remove('hidden')
        return
    }

    var url = '../profile/api/get/data/posts/'

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
            total_posts_recived += 1
            var last = data['others']['last']
            var posts = data['posts']

            var has = true
            if (posts == null) {
                //user has no posts
                var has = false
            }

            if (has) {
                for (i in posts) {

                    var item = ('<div style="max-width:33%;" data-loc="' + posts[i][0] + '"' + 'class="post p-1"><img style="width:100%; height:100%; margin-right:auto; margin-left:auto" src=' + posts[i][1] + '></div>')
                    document.getElementById('postss').innerHTML += item

                }
                if (last) {
                    document.getElementById('load_more_btn').classList.add('hidden')

                } else {

                    get_posts(time_itr + 1)

                }
            }

        })
}


get_posts(0)

function load_more_posts() {
    get_posts(0)
}
//This function

function get_tagged_posted(time_itrer) {

    document.getElementById('load_more_tagged').classList.add('hidden')
        //document.getElementById('tagged_btn').removeEventListener('click', 'HTMLElement')

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
            total_tagged_got += 1
            var has_tagged = data['is_tagged_in_any']

            if (!has_tagged) {} else {

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
    console.log(itr_time)
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
            book_marks_recived += 1

            if (!data['has_book_marks']) {

            } else {

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
            body: JSON.stringify({ 'deliverd': following_recived, 'user': user, 'per_call': 3 })
        })
        .then((resp) => {
            return resp.json()
        })
        .then((data) => {
            following_recived += data['others']['deliverd']
            if (!data['is_following_anyone']) {} else {
                var following = data['following']

                for (obj in following) {
                    if (following[obj].length == 2) {

                        item = ('<div style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + following[obj][0] + '" class="img-follower"><a class="follower-name">' + obj + '</a><br><button data-id="' + obj + '"class="btn btn-info remove-following">Unfollow</button><a href="#" class="follower-link" href="#">' + following[obj][1] + '</a> </div>')
                    } else {

                        item = ('<div style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + following[obj][0] + '" class="img-follower"><a class="follower-name">' + obj + '</a><br><button data-id="' + obj + '"class="btn btn-info remove-following">Unfollow</button><a href="#" class="follower-link" href="#">' + obj + '</a> </div>')
                    }
                    document.getElementById('following').innerHTML += item
                    add_remove_follower_func()
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
            followers_recived += data['others']['deliverd']
            if (!data['is_followed']) {

            } else {

                var followers = data['followers']

                for (obj in followers) {

                    if (followers[obj].length == 2) {
                        item = ('<div style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + followers[obj][0] + '"class="img-follower"><a class="follower-name">' + obj + '</a><br><i class="remove-follower   fa fa-close" data-id=' + obj + '></i><a href="#" class="follower-link" href="#">' + followers[obj][1] + '</a></div>')

                    } else {

                        item = ('<div style="display: block;margin:auto" class="follower bg-light p-2"><img src="' + followers[obj][0] + '" class="img-follower"><a class="follower-name">' + obj + '</a><br><i class="remove-follower  fa fa-close" data-id=' + obj + '></i><a href="#" class="follower-link" href="#">' + [obj] + '</a></div>')

                    }
                    document.getElementById('followers').innerHTML += item
                    add_unfollow_func()
                }

                if (data['others']['has_more']) {
                    get_following(time_itr + 1)
                } else {
                    return //No more Followers
                }
            }

        })


}

document.getElementById('tagged_btn').addEventListener('click', function() {
    get_tagged_posted(0)
})
document.getElementById('highlights_btn').addEventListener('click', function() {
    load_bookmarks(0)
})

document.getElementById('following_btn').addEventListener('click', function() {
    get_following(0)
})

document.getElementById('followers_btn').addEventListener('click', function() {
    get_followers(0)
})


function add_unfollow_func() {

    unfollow_buttons = document.getElementsByClassName('remove-follower ')
    for (var i = 0; i < unfollow_buttons.length; i++) {

        unfollow_buttons[i].addEventListener('click', function() {

            var username = this.dataset.id
            console.log(username)

        })

    }

}

function add_remove_follower_func() {

    unfollow_buttons = document.getElementsByClassName('remove-following')
    for (var i = 0; i < unfollow_buttons.length; i++) {

        unfollow_buttons[i].addEventListener('click', function() {

            var username = this.dataset.id
            console.log(username)

        })

    }

}

function remove_follower(username) {

    url = ''

    fetch(url, {

    })

}




function load_more_tagged_posts() {
    get_tagged_posted(0)
}