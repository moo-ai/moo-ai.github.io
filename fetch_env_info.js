onmessage = function(evt) {
    var octo = new Octokat({
        username: 'bzhaoopenstack',
        password: 'jingyibb1314~',
    })
    repo = octo.repos('moo-ai', 'moo-ai.github.io')
    var pr_commit_id = evt.data
    var ip = ''
    while (true) {
        repo.contents("env_info/" + pr_commit_id + ".json").read()
        var json_c_obj = JSON.parse(json_contents)
        var ip_str = json_c_obj['ip']
        ip = ip_str.split("\'")[1]
        var build_id = json_c_obj['build_id']
        if (ip != '') {
            break
        }
    }
    postMessage(ip + '|' + build_id)
}
