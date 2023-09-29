// Here the api routes for the web page backend will be stored

import { NextResponse } from 'next/server';

export async function POST(req) {

  try {
    
    const { start_point, end_point } = await req.json();

    
    let genereate_path = await fetch("localhost:80/generate",{
      method: "POST",
      headers: {
        "Content-Type": "application/json", //Required by flask server. 
      },
      body: JSON.stringify({ "start_point": start_point, "end_point": end_point}),
    });

    let generation_result = await genereate_path.json();
    let path = generation_result.path

    return NextResponse.json({body: JSON.stringify(path),status: 200})

  } catch (error) {
    return NextResponse.json({error: ("Error Occured During Path Generation: " + error), status: 500})
  }
}
