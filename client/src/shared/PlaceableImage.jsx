function PlaceableImage({src, alt=`image of ${src}`, top="", left="", bottom="", right="", width, height, position="absolute", transform, className }) {

    // RENDER //
    return (
      <img
        src={ src }
        alt={ alt }
        style={{ top, left, bottom, right, width, height, position, transform: transform || 'translateX(-50%)' }}
        className={className}
      />
    )
  
  }
  
  export default PlaceableImage
  
  // TO USE:
  //
  // <PlaceableImage
  //  src={saturn}
  //  alt='view of saturn'
  //  top='20vh'
  //  left='50vw'
  //  className='some-other-css-rules'
  // />
  //
  // IMPORTANT: this will automatically translate the item so that its horizontal
  // position is at its center
  