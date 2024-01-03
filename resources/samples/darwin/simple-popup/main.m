/*
    simple-popup - Simple popup example for demonstrating persistence on macOS.
*/

#import <Cocoa/Cocoa.h>


int main(int argc, const char * argv[]) {
    NSAlert *alert = [[NSAlert alloc] init];
    [alert setMessageText:@"Persistence Achieved!"];
    [alert addButtonWithTitle:@"OK"];

    NSImage *icon = [[NSImage alloc] initWithContentsOfFile:@"/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/public.generic-pc.icns"];
    if (icon != nil) {
        [alert setIcon:icon];
        [icon release];
    }

    [alert runModal];
    [alert release];

    return 0;
}