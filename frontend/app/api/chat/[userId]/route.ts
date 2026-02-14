import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ userId: string }> }
) {
  try {
    const { userId } = await params;
    const { message, conversation_id } = await req.json();

    // Get session server-side using Better Auth
    const reqHeaders = await headers();
    const session = await auth.api.getSession({
      headers: reqHeaders,
    });

    if (!session) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Fetch JWT token from Better Auth's token endpoint
    // Forward cookies to authenticate the token request
    const cookie = req.headers.get('cookie') || '';
    const tokenRes = await fetch(`${req.nextUrl.origin}/api/auth/token`, {
      method: 'GET',
      headers: {
        cookie,
      },
    });

    if (!tokenRes.ok) {
      console.error('Failed to get JWT token:', tokenRes.status);
      return NextResponse.json(
        { error: 'Failed to retrieve authentication token' },
        { status: 401 }
      );
    }

    const tokenData = await tokenRes.json();
    const jwtToken = tokenData.token;

    if (!jwtToken) {
      console.error('JWT token not found in response');
      return NextResponse.json(
        { error: 'Authentication token not available' },
        { status: 401 }
      );
    }

    // Forward the request to the Python backend with the JWT token
    const backendRes = await fetch(`${BACKEND_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${jwtToken}`,
      },
      body: JSON.stringify({
        message,
        conversation_id,
        user_id: userId,
      }),
    });

    if (!backendRes.ok) {
      const errorData = await backendRes.json();
      console.error('Backend error:', errorData);
      return NextResponse.json(
        { error: errorData.detail || 'Error from backend' },
        { status: backendRes.status }
      );
    }

    const data = await backendRes.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('API route error:', error);
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
