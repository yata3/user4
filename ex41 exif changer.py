import EXIF from 'exif-js';

const fileChangedHandler = (event) => {
    const files = event.target.files;
    console.log(files[0]);
    EXIF.getData(files[0], function () {
        console.log(EXIF.getAllTags(this));
    });
};


<input
    type="file"
    onChange={fileChangedHandler}
/> 
