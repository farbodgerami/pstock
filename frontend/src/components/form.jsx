 
import style from './form.module.css'
const Form = (props) => {
  return (
    <form onSubmit={props.onSubmit} style={props.style} className={style.form} >{props.children}</form>
  )
}

export default Form