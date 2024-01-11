export default function Navbar(props: any) {
  return (
    <nav className="bg-white border-gray-200 dark:bg-zinc-800">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4 ">
        <div className="flex items-center">
          <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">
            Virtual-PTZ
          </span>
        </div>
        {props.isOnline && (
          <button
            onClick={() => props.turnOff}
            className="inline-flex items-center px-2 py-1 mr-2 font-medium rounded dark:bg-green-800 dark:text-slate-300"
          >
            Turn off
          </button>
        )}
        {props.isOnline && (
          <span
            id="badge-dismiss-default"
            className="inline-flex items-center px-2 py-1 mr-2 font-medium rounded dark:bg-green-800 dark:text-slate-300"
          >
            Online
          </span>
        )}
        {!props.isOnline && (
          <span
            id="badge-dismiss-default"
            className="inline-flex items-center px-2 py-1 mr-2 font-medium rounded dark:bg-red-800 dark:text-slate-300"
          >
            Offline
          </span>
        )}
      </div>
    </nav>
  );
}
