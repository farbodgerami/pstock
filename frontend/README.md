very very important thing:
```js
const [formData,setFormData]=useState({firstname:"",lastname:""})
const handleChange =(e)=>{
setFormData({...formData,[e.target.name]:e.target.value})
}
```