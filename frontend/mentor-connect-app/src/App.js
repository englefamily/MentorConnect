import { useContext, useEffect, useRef, useState } from "react";
import SiteRoutes from "./SiteRoute";
import BaseNavbar from "./components/BaseNavbar";
import CategorySubcategoryDropdown from "./components/CategorySubcategoryDropdown";
import NewComponent from "./components/LoginModel";
import LoginModal from "./components/modals/LoginModal";
import context from "./Context";

function App() {
  const { showLoginModal, setShowLoginModal } = useContext(context);
  const [height, setHeight] = useState(0);
  const elementRef = useRef(null);

  useEffect(() => {
    // console.log(elementRef.current.clientHeight);
    // setHeight(elementRef.current.clientHeight);
  }, []);

    useEffect(() => {
      document.title = 'MentorConnect'; // Set the title here
      return () => {
        // Optionally, you can reset the title when the component unmounts
        document.title = 'MentorConnect';
      };
    }, []);

  return (
    <>
      <BaseNavbar />
      {showLoginModal && <LoginModal />}
      <SiteRoutes />
    </>
  );
}

export default App;
