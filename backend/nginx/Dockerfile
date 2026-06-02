FROM nginx:1.30.2-alpine

 

COPY default.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf

 



CMD ["nginx", "-g", "daemon off;"]
 