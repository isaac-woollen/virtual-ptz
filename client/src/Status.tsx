export default function Status(props: any) {
  return (
    <div className="grid grid-cols-2 text-xl mt-10 ml-auto mr-auto w-3/4 text-center gap-4 md:w-2/4 md:text-3xl">
      <div>
        <b>Last Action</b>
      </div>
      <div>{props.lastAction}</div>
      <div>
        <b>X Position</b>
      </div>
      <div>{props.xPOS}</div>
      <div>
        <b>Y Position</b>
      </div>
      <div>{props.yPOS}</div>
      <div>
        <b>X Speed</b>
      </div>
      <div>{props.xSpeed}</div>
      <div>
        <b>Y Speed</b>
      </div>
      <div>{props.ySpeed}</div>
    </div>
  );
}
