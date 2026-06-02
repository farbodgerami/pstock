import style from "./Main.module.css";
import LinkButton from "./LinkButton";
const Main = () => {
  return (
    
      <div className={style.body}>
        <h1>Stock Prediction App</h1>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit
          voluptatem animi dolorum optio corrupti expedita at quae doloremque
          excepturi molestiae minus ipsa magnam tenetur perspiciatis fugiat
          consectetur quasi, deserunt cupiditate ratione saepe neque doloribus
          praesentium. Officiis, fugit quidem harum dignissimos optio molestias
           
        </p>
        
<LinkButton buttonName='Explore Now' to='dashboard' className={style.mainButton}/>
      </div>
   
  );
};

export default Main;
