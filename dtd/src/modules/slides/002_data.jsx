
import React from 'react'

function Data() {

  return (
    <>
        <div className="h-screen w-full">
            <div className='
                h-full
                w-[60%]
                bg-white
                text-black
                mx-auto
                pt-[50px]
                overscroll-contain
            '>
                <div className='
                    w-full
                    h-full
                    flex
                    flex-row
                    justify-center
                    items-center
                '>
                    <div className=" w-full relative overflow-x-auto shadow-md border-[1px] sm:rounded-lg">
                        <table className="w-full text-sm text-left ">
                            <caption className="p-5 text-lg font-semibold text-left  text-gray-900 bg-white">
                                Flight Log
                                <p className="mt-1 text-sm font-normal text-gray-700 ">
                                A detailed list of every flight taken, noting when, where, why, and with who
                                </p>
                            </caption>
                            <thead className="text-xs bg-gray-50">
                                <tr>
                                    <th scope="col" className="px-6 py-3">
                                        Flight Number
                                    </th>                                
                                    <th scope="col" className="px-6 py-3">
                                        Date
                                    </th>
                                    <th scope="col" className="px-6 py-3">
                                        Airplane Model
                                    </th>
                                    <th scope="col" className="px-6 py-3">
                                        Tail Number
                                    </th>
                                    <th scope="col" className="px-6 py-3">
                                        Departure
                                    </th>
                                    <th scope="col" className="px-6 py-3">
                                        Arival
                                    </th>
                                    <th scope="col" className="px-6 py-3">
                                        Hours
                                    </th>
                                    <th scope="col" className="px-6 py-3">
                                        Memo
                                    </th>
                                    <th scope="col" className="px-6 py-3">
                                        ...
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                            <tr className="bg-white border-b hover:bg-black/5 ">
                                <td className="px-6 py-4">
                                        78
                                    </td>
                                    <td className="px-6 py-4">
                                        2013-04-29
                                    </td>
                                    <td className="px-6 py-4">
                                        PA44-180
                                    </td>
                                    <td className="px-6 py-4">
                                        N206AT
                                    </td>
                                    <td className="px-6 py-4">
                                        KVGT
                                    </td>
                                    <td className="px-6 py-4">
                                        Local
                                    </td>
                                    <td className="px-6 py-4">
                                        1.2
                                    </td>
                                    <td className="px-6 py-4">
                                        Multi Engine Manuvers
                                    </td>
                                    <td className="px-6 py-4">
                                        ...
                                    </td>
                                </tr>
                                <tr className="bg-white border-b hover:bg-black/5">
                                <td className="px-6 py-4">
                                        766
                                    </td>
                                    <td className="px-6 py-4">
                                        2021-06-19
                                    </td>
                                    <td className="px-6 py-4">
                                        C177
                                    </td>
                                    <td className="px-6 py-4">
                                        N1541H
                                    </td>
                                    <td className="px-6 py-4">
                                        KSGU
                                    </td>
                                    <td className="px-6 py-4">
                                        Local
                                    </td>
                                    <td className="px-6 py-4">
                                        1.7
                                    </td>
                                    <td className="px-6 py-4">
                                        C177 Intro with Ed Lewis
                                    </td>
                                    <td className="px-6 py-4">
                                        ...
                                    </td>
                                </tr>
                                <tr className="bg-white border-b hover:bg-black/5">
                                <td className="px-6 py-4">
                                        1366
                                    </td>
                                    <td className="px-6 py-4">
                                        2022-05-19
                                    </td>
                                    <td className="px-6 py-4">
                                        C172
                                    </td>
                                    <td className="px-6 py-4">
                                        N5378D
                                    </td>
                                    <td className="px-6 py-4">
                                        1L8
                                    </td>
                                    <td className="px-6 py-4">
                                        KSGU
                                    </td>
                                    <td className="px-6 py-4">
                                        0.6
                                    </td>
                                    <td className="px-6 py-4">
                                        Recreational Pilot PTS with Tim Leeny 
                                    </td>
                                    <td className="px-6 py-4">
                                        ...
                                    </td>
                                </tr>
                                <tr className="bg-white border-b hover:bg-black/5">
                                <td className="px-6 py-4">
                                        1612
                                    </td>
                                    <td className="px-6 py-4">
                                        2022-10-15
                                    </td>
                                    <td className="px-6 py-4">
                                        C172
                                    </td>
                                    <td className="px-6 py-4">
                                        N5378D
                                    </td>
                                    <td className="px-6 py-4">
                                        KSGU
                                    </td>
                                    <td className="px-6 py-4">
                                        KKNB
                                    </td>
                                    <td className="px-6 py-4">
                                        1.0
                                    </td>
                                    <td className="px-6 py-4">
                                        Cross country Traing with Rick Kasper
                                    </td>
                                    <td className="px-6 py-4">
                                        ...
                                    </td>
                                </tr>
                                <tr className="bg-white border-b hover:bg-black/5">
                                <td className="px-6 py-4">
                                        2133
                                    </td>
                                    <td className="px-6 py-4">
                                        2023-08-31
                                    </td>
                                    <td className="px-6 py-4">
                                        PA28-181
                                    </td>
                                    <td className="px-6 py-4">
                                        N8342N
                                    </td>
                                    <td className="px-6 py-4">
                                        KSGU
                                    </td>
                                    <td className="px-6 py-4">
                                        KKNB
                                    </td>
                                    <td className="px-6 py-4">
                                        0.8
                                    </td>
                                    <td className="px-6 py-4">
                                        Archer Checkout for Jonathan Demke
                                    </td>
                                    <td className="px-6 py-4">
                                        ...
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </>
  )
}

export default Data
