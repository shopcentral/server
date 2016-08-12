using UnityEngine;
using UnityEditor;
using System.Collections;

public class CreateAssetBundles
{
    [MenuItem ("Assets/Build AssetBundles")]
    static void BuildAllAssetBundles ()
    {
        BuildPipeline.BuildAssetBundles ("Assets/AssetBundles", BuildAssetBundleOptions.None, BuildTarget.StandaloneOSXUniversal);
    }
}
public class builder : MonoBehaviour {

	public string platform;
	public string file;
	public GameObject[] objs;
	// Use this for initialization
	void Start () {

	}
	void Builder(){


	}
	// Update is called once per frame
	void Update () {
			if (Input.GetKeyDown (KeyCode.B))
				Builder ();
	}
}
