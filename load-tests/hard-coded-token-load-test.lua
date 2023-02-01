wrk.method = "POST"

-- post form urlencoded data
wrk.body = "x=[0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0]"
wrk.headers['Authorization'] = "bearer <gcloud-bearer-token>" -- Replace with your own token
wrk.headers['Content-Type'] = "application/json"
