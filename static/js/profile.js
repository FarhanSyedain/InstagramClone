function include(file) {

    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;

    document.getElementsByTagName('head').item(0).appendChild(script);

}

include('../static/js/backend.js')
include('../static/js/home.js')

url = 'profile/api/get/data/posts/'

get_posts()

if (total_posts == '0') {

    document.getElementById('postss').innerHTML = '<h1>This user has no posts</h1>'

} else {

    while (true) {
        data = get_posts()

        if (data['last']) {
            break
        } else {
            posts = data['posts']
            console.log(posts)

        }
    }
    console.log('Finish')

}

function get_posts() {
    console.log('Called me' + 'hlo tiem')
    return { 'last': false, 'posts': ['f', 'f', 'f'] }

}