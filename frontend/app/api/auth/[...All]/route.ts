/**
 * Task T-237: Better Auth API route handler
 *
 * This route mounts the Better Auth handler at /api/auth/[...all]
 * All authentication requests go through this handler
 */

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest, NextResponse } from "next/server";

/**
 * Export GET and POST handlers for all auth routes
 * This creates the following endpoints:
 * - POST /api/auth/sign-up
 * - POST /api/auth/sign-in
 * - POST /api/auth/sign-out
 * - GET /api/auth/session
 * - etc.
 */

// Wrap the handlers to catch database errors
const { GET: baseGET, POST: basePOST } = toNextJsHandler(auth.handler);

export async function GET(request: NextRequest) {
  try {
    console.log("[Auth Route] GET request to:", request.nextUrl.pathname);
    return await baseGET(request);
  } catch (error) {
    console.error("[Auth Route] GET error:", error);
    if (error instanceof Error && error.message.includes("database")) {
      console.error(
        "[Auth Route] Database connection failed. Check DATABASE_URL in .env.local"
      );
      // Return graceful error response instead of throwing
      return NextResponse.json(
        { error: "Authentication service temporarily unavailable" },
        { status: 503 }
      );
    }
    // Return generic error for unexpected failures
    return NextResponse.json(
      { error: "Authentication service error" },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    console.log("[Auth Route] POST request to:", request.nextUrl.pathname);
    const response = await basePOST(request);
    console.log("[Auth Route] POST response status:", response.status);
    return response;
  } catch (error) {
    console.error("[Auth Route] POST error:", error);
    if (error instanceof Error) {
      console.error("[Auth Route] Error message:", error.message);
      // Only log stack in development to avoid exposing internals in production
      if (process.env.NODE_ENV === "development") {
        console.error("[Auth Route] Error stack:", error.stack);
      }
      if (error.message.includes("database")) {
        console.error(
          "[Auth Route] Database connection failed. Check DATABASE_URL in .env.local"
        );
        // Return graceful error response for database issues
        return NextResponse.json(
          { error: "Authentication service temporarily unavailable" },
          { status: 503 }
        );
      }
    }
    // Return generic error for unexpected failures
    return NextResponse.json(
      { error: "Authentication service error" },
      { status: 500 }
    );
  }
}
