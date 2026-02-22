import { NextResponse } from 'next/server';
import { execSync } from 'child_process';
import path from 'path';

export async function POST(request) {
    const body = await request.json();

    try {
        // Path to the master recommender script
        const scriptPath = path.join(process.cwd(), '..', 'main_recommender.py');
        const cwd = path.join(process.cwd(), '..');

        // Execute the Python script and pass preferences as JSON via stdin
        const inputJson = JSON.stringify(body);
        const output = execSync(`python main_recommender.py`, {
            cwd: cwd,
            input: inputJson,
            encoding: 'utf-8'
        });

        const result = JSON.parse(output);

        if (result.error) {
            return NextResponse.json({ error: result.error }, { status: 500 });
        }

        // Map AI insight to individual recommendations for better UI display
        if (result.ai_insight && !result.ai_insight.startsWith("Error")) {
            result.recommendations = result.recommendations.map(res => ({
                ...res,
                description: result.ai_insight.slice(0, 200) + "..." // Simplified mapping for now
            }));
        }

        return NextResponse.json(result);
    } catch (error) {
        console.error("Backend Error:", error);
        return NextResponse.json({
            error: "Failed to fetch recommendations from AI engine.",
            details: error.message
        }, { status: 500 });
    }
}
