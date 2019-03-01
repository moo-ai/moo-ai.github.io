onmessage = function(evt) {
    const sleep = (milliseconds) => {
        return new Promise(resolve => setTimeout(resolve, milliseconds))
    }
    var pr_commit_id = evt.data
    var ip = 'none'
    var build_id = 'none'
    var no_content = true
    var env_request

    var zuul_request = new XMLHttpRequest()
    zuul_request.onreadystatechange = function() {
        if (zuul_request.readyState === 4) {
            if (zuul_request.status === 200) {
                zuul_data = zuul_request.responseText
                parsed_zuul_data = JSON.parse(zuul_data)
                if (parsed_zuul_data.length != 0) {
                    status_cell.innerHTML = parsed_zuul_data[0]['result']
                }
            }

        }
    }
    zuul_request.open('GET', zuul_host + 'api/buildsets?project=moo-ai/moo-ai.github.io&patchset=' + row_data[
        "patch_set"], true)
    zuul_request.send()
}
}
