/**
 * Copyright 2020 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

package integration;

import static org.junit.Assert.assertTrue;

import java.io.File;
import java.io.IOException;

import org.json.JSONObject;
import org.junit.BeforeClass;
import org.junit.ClassRule;
import org.junit.Test;
import org.skyscreamer.jsonassert.JSONAssert;
import org.skyscreamer.jsonassert.JSONCompareMode;

import org.testcontainers.containers.DockerComposeContainer;

import integration.util.TestHelper;

public class IntegrationTest {
    
    @ClassRule
    public static DockerComposeContainer docker =
        new DockerComposeContainer(new File("build/resources/test/docker/docker-compose.yml"))
            .withLocalCompose(true);

    @BeforeClass
    public static void initialize() throws IOException, InterruptedException {
        TestHelper.initializeXLR("docker/initialize/data/release-template.json");
    }

    // Tests

    @Test
    public void testSetVariables() throws Exception 
    {
        JSONObject theResult = TestHelper.getReleaseResult();
        assertTrue(theResult != null);

        String expected = TestHelper.readFile(VarSetterTestHelper.getResourceFilePath("testExpected/test1.json"));

        JSONAssert.assertEquals(expected, theResult, JSONCompareMode.NON_EXTENSIBLE);
    }
}
