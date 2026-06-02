import style from "./LinkButton.module.css";
import { Link } from "react-router-dom";
const LinkButton = (props) => {
  return (
 
    <Link className={`${style.linkBotton} ${props.className}`} onClick={props.onClick} to={props.to}>{props.buttonName}</Link>
  )
}

export default LinkButton