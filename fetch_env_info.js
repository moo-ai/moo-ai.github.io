onmessage = function(evt) {
    const sleep = (milliseconds) => {
        return new Promise(resolve => setTimeout(resolve, milliseconds))
    }
    var pr_commit_id = evt.data
    var ip = ''
    var build_id = ''
    var no_content = true
    var env_request
    while (no_content) {
        sleep(10000).then(() => {
            env_request = new XMLHttpRequest()
            env_request.onreadystatechange = function() {
                if (env_request.readyState === 4) {
                    if (env_request.status === 200) {
                        var json_c_obj = JSON.parse(env_request.responseText)
                        var ip_str = json_c_obj['ip']
                        ip = ip_str.split("\'")[1]
                        build_id = json_c_obj['build_id']

                        no_content = false
                        postMessage([ip, build_id])
                    }
                }
            }
            env_request.open('GET', '/env_info/' + pr_commit_id + '.json', false)
            env_request.send()
        })
    }
}
