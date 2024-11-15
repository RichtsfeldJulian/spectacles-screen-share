@component
export class ScreenViewer extends BaseScriptComponent {
  @input
  remoteServiceModule: RemoteServiceModule;

  @input
  image: Image;

  private remoteMediaModule: RemoteMediaModule = require("LensStudio:RemoteMediaModule");

  private updateInterval: number = 0.3; // Poll every 1s
  private isLoading: boolean = false;
  private updateEvent = this.createEvent("UpdateEvent");
  private sumDeltaTime: number;

  onAwake() {
    this.updateEvent.bind((eventData) => {
      this.sumDeltaTime += eventData.getDeltaTime();

      if (this.isLoading || this.sumDeltaTime < this.updateInterval) {
        return;
      }
      this.isLoading = true;
      this.sumDeltaTime = 0;

      // Create HTTP request
      const httpRequest = RemoteServiceHttpRequest.create();
      httpRequest.url = "https://screen-capture-server.azurewebsites.net/screen/pc.jpg";
      httpRequest.method = RemoteServiceHttpRequest.HttpRequestMethod.Get;

      // Perform the HTTP request
      this.remoteServiceModule.performHttpRequest(httpRequest, (response) => {
        this.isLoading = false;
        if (response.statusCode === 200) {
          // Check if the response status is 200 (OK)
          let textureResource = response.asResource(); // Convert the response to a resource
          this.remoteMediaModule.loadResourceAsImageTexture(
            textureResource,
            (texture) => {
              // Assign texture to a material
              this.image.mainPass.baseTex = texture;
            },
            (error) => {
              print("Error loading image texture: " + error); // Print an error message if loading fails
            }
          );
        } else {
          print("Error loading image status: " + response.statusCode);
        }
      });
    });
  }
}
